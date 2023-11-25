import time
from typing import Generator
import itertools
from loguru import logger as log
import os
from functools import cache, cached_property
import base64
import lzma
import tqdm
import io
import grequests
import requests
import pandas as pd
from rdflib.plugins.sparql.results.jsonresults import JSONResultParser
import functools
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.compute as pc
import pyarrow.parquet as pq
from pyarrow import fs
import rdflib


class Client:
    """
    Client class for interacting with the Mortar Data API.
    """
    def __init__(self) -> None:
        # monkey-patch RDFlib to deal with some issues w.r.t. oxrdflib
        def namespaces(self):
            if not self.store.namespaces():
                return []
            for prefix, namespace in self.store.namespaces():
                namespace = rdflib.URIRef(namespace)
                yield prefix, namespace

        rdflib.namespace.NamespaceManager.namespaces = namespaces

        self._s3 = fs.S3FileSystem(region=os.getenv("MORTARDATA_S3_REGION"))
        self._bucket = os.getenv("MORTARDATA_S3_BUCKET")
        self._sparql_endpoint = os.getenv("MORTARDATA_QUERY_ENDPOINT")
        self._sites_endpoint = os.getenv("MORTARDATA_SITES_ENDPOINT")
        
        self.ds = ds.parquet_dataset(
            f"{self._bucket}/_metadata", partitioning="hive", filesystem=self._s3
        )
        log.info("Connected to Parquet dataset")

    def _table_exists(self, table: str) -> bool:
        """
        Check if a table exists in the data cache.

        Args:
            table (str): The name of the table.

        Returns:
            bool: True if the table exists, False otherwise.
        """
        try:
            res = self.data_cache.table(table)
            return res is not None
        except RuntimeError:
            return False

    @cached_property
    def sites(self) -> list:
        """
        Get the list of sites.

        Returns:
            list: The list of sites.
        """
        t0 = time.time()
        res = requests.get(self._sites_endpoint)
        sites = res.json()
        log.info(f"Fetched {len(sites)} sites in {time.time()-t0:.2f}sec")
        return sites


    def sparql(self, query: str, sites: list = None) -> pd.DataFrame:
        """
        Execute a SPARQL query.

        Args:
            query (str): The SPARQL query.
            sites (list, optional): The list of sites to query. Defaults to None.

        Returns:
            pd.DataFrame: The result of the query.
        """
        body = {'query': query}
        if sites is not None:
            body['sites'] = sites
            log.info(f"Dispatching parallel SPARQL queries for {len(sites)} sites")
            sparql_requests = (
                grequests.post(self._sparql_endpoint, json={'query': query, 'sites': [site]})
                for site in sites
            )
            responses = grequests.imap(sparql_requests, size=len(sites))
            dfs = []
            for res in responses:
                if not res.ok:
                    raise Exception(res.content)
                b = io.BytesIO(lzma.decompress(base64.urlsafe_b64decode(res.content)))
                resp = JSONResultParser().parse(b)
                df = pd.DataFrame.from_records(list(resp), columns=[str(c) for c in resp.vars])
                log.info(f"Fetched {len(df)} SPARQL rows")
                dfs.append(df)
            return functools.reduce(lambda x, y: pd.concat([x, y], axis=0), dfs)
        res = requests.post(self._sparql_endpoint, json=body)
        if not res.ok:
            raise Exception(res.content)
        b = io.BytesIO(lzma.decompress(base64.urlsafe_b64decode(res.content)))
        res = JSONResultParser().parse(b)
        df = pd.DataFrame.from_records(list(res), columns=[str(c) for c in res.vars])
        return df

    def _to_batches(self, sparql: str, sites: list = None, start: str = None, end: str = None, limit: int = None) -> Generator:
        """
        Convert a SPARQL query to batches.

        Args:
            sparql (str): The SPARQL query.
            sites (list, optional): The list of sites to query. Defaults to None.
            start (str, optional): The start time. Defaults to None.
            end (str, optional): The end time. Defaults to None.
            limit (int, optional): The maximum number of results. Defaults to None.

        Returns:
            Generator: A generator that yields batches of results.
        """
        res = self.sparql(sparql, sites=sites)
        start = pd.to_datetime("2000-01-01T00:00:00Z" if not start else start)
        end = pd.to_datetime("2100-01-01T00:00:00Z" if not end else end)
        uuids = list(set([str(item) for row in res.values for item in row]))
        f = (
            (ds.field("uuid").isin(uuids))
            & (ds.field("time") <= pa.scalar(end, type=pa.timestamp("us", tz="UTC")))
            & (ds.field("time") >= pa.scalar(start, type=pa.timestamp("us", tz="UTC")))
        )
        if sites is not None:
            print([s[4:-1] for s in sites])
            log.info(f"Fetching data for {sites} with {start=} {end=} ({limit=})")
            f &= ds.field("collection").isin([s[4:-1] for s in sites])


        batches_iter = self.ds.to_batches(
            columns=["time", "value", "collection", "uri"], filter=f
        )
        # apply limit; note that this is not a hard limit, since we may have to
        # fetch more data to get the requested number of records
        for batch in tqdm.tqdm(
            batches_iter,
            desc="Downloading data from s3",
            unit="batches",
        ):
            # check if we've downloaded enough records
            if limit is not None and limit <= 0:
                continue
            if limit is not None:
                # update limit to reflect the number of records we've already
                # downloaded
                limit -= batch.num_rows
            yield batch
        # close batches
        batches_iter.close()

    def data_sparql_to_csv(
        self, sparql: str, filename: str, sites: list = None, start: str = None, end: str = None, limit: int = None
    ) -> int:
        """
        Execute a SPARQL query and save the results to a CSV file.

        Args:
            sparql (str): The SPARQL query.
            filename (str): The name of the CSV file to save the results to.
            sites (list, optional): The list of sites to query. Defaults to None.
            start (str, optional): The start time. Defaults to None.
            end (str, optional): The end time. Defaults to None.
            limit (int, optional): The maximum number of results. Defaults to None.

        Returns:
            int: The number of records downloaded.
        """
        """
        returns the number of records downloaded
        """
        num = 0
        for batch in self._to_batches(
            sparql, sites=sites, start=start, end=end, limit=limit
        ):
            df = batch.to_pandas()
            num += len(df)
            df.to_csv(filename, mode="a", header=False)
        return num

    def data_sparql_to_duckdb(
        self, sparql: str, database: str, table: str, sites: list = None, start: str = None, end: str = None, limit: int = None
    ) -> "duckdb.DuckDBPyConnection":
        """
        Execute a SPARQL query and save the results to a DuckDB database.

        Args:
            sparql (str): The SPARQL query.
            database (str): The name of the DuckDB database to save the results to.
            table (str): The name of the table to save the results to.
            sites (list, optional): The list of sites to query. Defaults to None.
            start (str, optional): The start time. Defaults to None.
            end (str, optional): The end time. Defaults to None.
            limit (int, optional): The maximum number of results. Defaults to None.

        Returns:
            duckdb.DuckDBPyConnection: The DuckDB connection.
        """
        # handle the case where duckdb is not installed
        try:
            import duckdb
        except ImportError:
            raise Exception("duckdb is not installed. Please install it with `pip install duckdb`")

        self.data_cache = duckdb.connect(database)
        for batch in self._to_batches(
            sparql, sites=sites, start=start, end=end, limit=limit
        ):
            pq.write_table(pa.Table.from_batches([batch]), "tmp.parquet")
            if not self._table_exists(table):
                self.data_cache.execute(
                    f"CREATE TABLE {table} AS SELECT * from parquet_scan('tmp.parquet')"
                )
            else:
                self.data_cache.execute(
                    f"INSERT INTO {table} SELECT * from parquet_scan('tmp.parquet')"
                )
            os.remove("tmp.parquet")
        self.data_cache.commit()
        return self.data_cache.table(table)

    def data_sparql(self, sparql: str, sites: list = None, start: str = None, end: str = None, limit: int = None) -> pd.DataFrame:
        """
        Execute a SPARQL query and return the results as a DataFrame.

        Args:
            sparql (str): The SPARQL query.
            sites (list, optional): The list of sites to query. Defaults to None.
            start (str, optional): The start time. Defaults to None.
            end (str, optional): The end time. Defaults to None.
            limit (int, optional): The maximum number of results. Defaults to None.

        Returns:
            pd.DataFrame: The result of the query.
        """
        dfs = []
        for batch in self._to_batches(
            sparql, sites=sites, start=start, end=end, limit=limit
        ):
            df = batch.to_pandas()
            dfs.append(df)
        if len(dfs) == 0:
            return pd.DataFrame()
        if len(dfs) == 1:
            return dfs[0]
        return functools.reduce(lambda x, y: pd.concat([x, y], axis=0), dfs)


if __name__ == "__main__":
    c = Client()
    
    all_points = """
        PREFIX brick: <https://brickschema.org/schema/Brick#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?point ?type ?uuid WHERE {
        ?point rdf:type/rdfs:subClassOf* brick:Point ;
                   rdf:type ?type ;
                   brick:timeseries [ brick:hasTimeseriesId ?uuid ] .
    }"""
    df = c.sparql(all_points)
    df.to_csv("all_points.csv")
    print(df.head())

    query1 = """
        PREFIX brick: <https://brickschema.org/schema/Brick#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?sen_point ?sen WHERE {
        ?sen_point rdf:type brick:Supply_Air_Temperature_Sensor ;
                   brick:timeseries [ brick:hasTimeseriesId ?sen ] .
    }"""
    df = c.sparql(query1)
    df.to_csv("query1_sparql.csv")
    print(df.head())

    df = c.data_sparql(query1, start="2016-01-01", end="2016-02-01", limit=1e6, sites=['bldg2','bldg5'])
    print(df.head())

    res = c.data_sparql_to_csv(query1, "query1.csv", sites=['bldg2','bldg5'])
    print(res)
