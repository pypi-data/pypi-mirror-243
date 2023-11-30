import pandas
import clickhouse_connect
from pandas import DataFrame
from nazca4sdk.datahandling.hotstorage.query import Query
from dependency_injector.wiring import inject


class ClickhouseClient:
    @inject
    def __init__(self, host: str, port: str):
        self._clickhouse_port = int(port)
        self._host = host

    def get(self, query: Query) -> DataFrame:
        client = clickhouse_connect.get_client(host=self._host,
                                               port=self._clickhouse_port,
                                               username='readonly',
                                               password='I6DSw4oMO79loo8T')
        query = str(query)
        df_stream = client.query_df_stream(query)
        dataframes = pandas.DataFrame()
        with df_stream:
            for df in df_stream:
                dataframes = pandas.concat([dataframes, df])
        return dataframes
