""" Data_mod module"""
import pandas as pd
from dask import dataframe


class Data:
    """
    Modification structure of data received from OpenData
    """

    def __init__(self, variable):
        self.__data = variable

    def to_df(self):
        """
        Returns DataFrame from received input

        Example:
            df = Data(selected_data).to_df()
        """
        if self.__is_empty():
            return []
        data_df = pd.json_normalize(self.__data)

        try:
            if 'measureTime' in data_df.columns:
                return data_df.sort_values(by='measureTime', ascending=True, ignore_index=True)
        except NameError:
            print('Error, measureTime column missing in dataframe')

    def data_to_list(self):
        """
        Method to modify data structure to list
        """

        return self.__data.values.tolist()

    def data_to_numpy(self):
        """
        Method to modify data structure to numpy array
        """

        return self.__data.to_numpy()

    def __is_empty(self):
        return len(self.__data) == 0

    def to_dask_df(self):

        if self.__is_empty():
            return []

        d1 = self.__data[0]
        ds = []

        for i in range(len(self.__data)):
            ds.append(self.__data[i])

        d = {}
        for k in d1.keys():
            d[k] = tuple(d[k] for d in ds)

        data_df = dataframe.from_dict(d, orient="columns", npartitions=1).reset_index(drop=True)

        try:
            if 'measureTime' in data_df.columns:
                data_df = data_df.sort_values(by='measureTime', ascending=True, ignore_index=True).reset_index(
                    drop=True)
                return data_df
        except NameError:
            print('Error, measureTime column missing in dataframe')

    def to_pivot_df(self):
        if self.__is_empty():
            return []
        try:
            CH_COLUMNS = ["Module", "MeasureTime", "Variable", "Value"]
            df = pd.DataFrame(self.__data, columns=CH_COLUMNS)
        except NameError:
            print('Error, name of columns are incorrect')

        df["Value"] = pd.to_numeric(df.Value)
        return df.pivot_table(index='MeasureTime', columns='Variable', values='Value')
