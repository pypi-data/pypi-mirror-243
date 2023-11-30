from datetime import datetime, timedelta
from tzlocal import get_localzone
from typing import Optional, List

from pandas import DataFrame

from nazca4sdk.datahandling.hotstorage.clickhouse.clickhouse_client import ClickhouseClient
from nazca4sdk.datahandling.hotstorage.query import Query
from nazca4sdk.datahandling.kafka.kafka_sender import KafkaSender
from nazca4sdk.datahandling.npoe.connection import Connections
from nazca4sdk.datahandling.npoe.hot_storage_value import HotStorageValue
from nazca4sdk.datahandling.npoe.query_helper import NpoeQueryHelper
from nazca4sdk.datahandling.open_data_client import OpenDataClient
from nazca4sdk.datahandling.variable_verificator import VariableIntervalInfo, DATE_TIME_FORMAT, \
    VariableIntervalSubtractionInfo, ElectricMetersDataValidator, PgAvgDataValidator, SsvSopOrderedPowerDataValidator, \
    OrganizationCo2DataValidator, OzeConnectionInvertersDataValidator, OzeConnectionsForMetersDataValidator, \
    OzeInvertersSummaryDataValidator, MetersDataValidator

from nazca4sdk.system.system_cache import SystemCache
from nazca4sdk.tools.time import get_time_delta
from dependency_injector.wiring import inject


class Npoe:
    """ Class to get data from npoe

    """

    @inject
    def __init__(self, cache: SystemCache,
                 opendata_client: OpenDataClient,
                 click: ClickhouseClient,
                 broker: KafkaSender):
        self._system_cache = cache
        self._clickhouse_client = click
        self._openData = opendata_client
        self._broker = broker

    def get_electric_meters_data(self, system_name: List[str], variables=None, **time: dict) -> Optional[DataFrame]:
        """
        Gets electric meters data in specific time range

        Args:
            system_name: list of electric meter devices,
            variables: list of electric meter variables
            time: possible pairs - start_date, end_date or time_amount, time_unit

        Returns:
            DataFrame: values for selected variables and time range

        Examples:
            read(system_name:["module"], start_date="2023-03-21TOO:OO:00")
            read(system_name:["module"], time_amount=1,time_unit="MINUTE")
            read(system_name:["module"], time_amount=1, time_unit="MINUTE", variables=["U1","U2"])
        """
        if variables is None:
            variables = []
        keys = time.keys()

        columns_to_validate = {'system_name': system_name, 'variables': variables}
        columns_info = ElectricMetersDataValidator(**columns_to_validate)
        if "start_date" in keys and "end_date" in keys:
            time_to_validate = {'start_date': time.get("start_date"),
                                'end_date': time.get("end_date")}

            time_info = VariableIntervalInfo(**time_to_validate)
            return self._get_electric_meters_data(
                system_names=columns_info.system_name,
                start_date=datetime.strptime(time_info.start_date, DATE_TIME_FORMAT),
                end_date=datetime.strptime(time_info.end_date, DATE_TIME_FORMAT),
                variables=columns_info.variables)

        elif "time_amount" in keys and "time_unit" in keys:
            time_to_validate = {'time_amount': time.get("time_amount"),
                                'time_unit': time.get("time_unit")}

            variable_info = VariableIntervalSubtractionInfo(**time_to_validate)
            end_date = datetime.now()
            start_date = end_date - get_time_delta(variable_info.time_unit, variable_info.time_amount)

            return self._get_electric_meters_data(
                system_names=system_name,
                start_date=start_date,
                end_date=end_date,
                variables=variables)

        print("time should contains start_date and end_date or time_unit and time_amount")
        return None

    def _get_electric_meters_data(self, system_names, start_date, end_date, variables) -> Optional[DataFrame]:
        """
        Gets electric meters variables in specific time range by connection with open database

        Args:
            system_names - electric meter names,
            start_time - beginning of the time range,
            stop_time - ending of the time range,
            variables - list of electric meter variables

        Returns:
            DataFrame: values for selected variable and time range

        """
        if variables is None:
            variables = []
        try:
            if len(variables) == 0:
                query = Query() \
                    .SELECT("*") \
                    .FROM(f"npoe.electric_meters_raw") \
                    .WHERE(f"SystemName IN ({system_names}) "
                           f"AND MeasureTime >= '{start_date.strftime('%Y-%m-%dT%H:%M:%S')}' "
                           f"AND MeasureTime <= '{end_date.strftime('%Y-%m-%dT%H:%M:%S')}' ")
            else:
                selected_columns = "SystemName, MeasureTimeLong, MeasureTime, MeasureTimeUtc," + ','.join(variables)
                query = Query() \
                    .SELECT(selected_columns) \
                    .FROM(f"npoe.electric_meters_raw") \
                    .WHERE(f"SystemName IN ({system_names}) "
                           f"AND MeasureTime >= '{start_date.strftime('%Y-%m-%dT%H:%M:%S')}' "
                           f"AND MeasureTime <= '{end_date.strftime('%Y-%m-%dT%H:%M:%S')}' ")

            df = self._clickhouse_client.get(query)

            if df.size > 0:
                df = df.sort_values('MeasureTime').reset_index(drop=True)

            return df
        except ValueError:
            print("Error - Get variable data from Nazca4")
            return None

    def get_pgavg_data(self, connection: str, **time: dict) -> Optional[DataFrame]:
        """
        Gets power_guard_agg_hour values in specific time range

        Args:
            connection: list of electric meter devices,
            time: possible pair - start_date, end_date

        Returns:
            DataFrame: values for selected connection and time range
        """

        keys = time.keys()
        if "start_date" in keys and "end_date" in keys:
            if 'Z' in time.get("start_date"):
                datetime_start_obj = datetime.strptime(time.get("start_date"), "%Y-%m-%dT%H:%M:%S.%fZ")
                start_date = datetime_start_obj.strftime("%Y-%m-%dT%H:%M:%S")

                datetime_end_obj = datetime.strptime(time.get("end_date"), "%Y-%m-%dT%H:%M:%S.%fZ")
                end_date = datetime_end_obj.strftime("%Y-%m-%dT%H:%M:%S")

                columns_to_validate = {'connection': connection, 'start_date': start_date, 'end_date': end_date}
            else:
                columns_to_validate = {'connection': connection, 'start_date': time.get("start_date"),
                                       'end_date': time.get("end_date")}
            columns_info = PgAvgDataValidator(**columns_to_validate)

            return self._get_pgavg_data(
                connection=columns_info.connection,
                start_date=datetime.strptime(columns_info.start_date, DATE_TIME_FORMAT),
                end_date=datetime.strptime(columns_info.end_date, DATE_TIME_FORMAT))
        else:
            print("time should contains start_date and end_date")
            return None

    def _get_pgavg_data(self, connection, start_date, end_date) -> Optional[DataFrame]:
        """
        Gets power_guard_agg_hour values in specific time range by connection with open database

        Args:
            connection - SystemName from database,
            start_date - beginning of the date range,
            end_date - ending of the date range,

        Returns:
            DataFrame: values for selected time range
        """
        try:
            query = Query() \
                .SELECT("MeasureTimeUtc, Pt_Window_Max as value") \
                .FROM(f"npoe.power_guard_agg_hour") \
                .WHERE(f"Connection LIKE '{connection}' "
                       f"AND MeasureTimeUtc >= '{start_date.strftime('%Y-%m-%dT%H:%M:%S')}' "
                       f"AND MeasureTimeUtc <= '{end_date.strftime('%Y-%m-%dT%H:%M:%S')}'")
            df = self._clickhouse_client.get(query).sort_values('MeasureTimeUtc').reset_index(drop=True)
            return df
        except Exception:
            raise ValueError(f"Error - Get variable data from Nazca4")

    def get_ssv_sop_orderedpower(self, connection) -> Optional[DataFrame]:
        """
        Gets Ssv, Sop, OrderedPower values for specific connection from database

        Args:
            connection: list of electric meter devices,

        Returns:
            DataFrame: Ssv, Sop, OrderedPower values for selected connection
        """
        columns_to_validate = {'connection': connection}
        columns_info = SsvSopOrderedPowerDataValidator(**columns_to_validate)

        return self._get_ssv_sop_orderedpower(connection=columns_info.connection)

    def _get_ssv_sop_orderedpower(self, connection) -> Optional[DataFrame]:
        try:
            if len(connection) != 0:
                query = Query() \
                    .SELECT("SOP, SSV, OrderedPower") \
                    .FROM(f"npoe.db_connections") \
                    .WHERE(f"SystemName LIKE '{connection}'")

                df = self._clickhouse_client.get(query)
            return df
        except ValueError:
            print("Error - Get connection data from Nazca4")
            return None

    def calculate_pt_max_window(self):
        """
        Calculate max window value from electric meters connections power total 15min averages
        and save results to hotstorage
        """
        self._calculate_pt_max_window()

    def _calculate_pt_max_window(self):
        try:
            end_date = datetime.utcnow().replace(minute=0, second=0)
            start_date = end_date - timedelta(hours=1)
            query = NpoeQueryHelper().get_pt_max_window_query(start_date, end_date)

            df = self._clickhouse_client.get(query)

            data = []
            for i, row in df.iterrows():
                variables = [row.Connection, row.MeasureTime.strftime("%Y-%m-%dT%H:%M:%S"),
                             row.MeasureTimeUtc.strftime("%Y-%m-%dT%H:%M:%S"), row.Time_Inc, row.Pt_Window_Max]
                data.append(variables)

            self._broker.send_message(topic="dataflow.fct.clickhouse",
                                      key="sdk npoe",
                                      data=[HotStorageValue(table_name="npoe.power_guard_agg_hour", data=data).__dict__]
                                      )
            return df
        except Exception:
            print("Error - Calculate pt max window")
            return None

    def check_boot_profiles_to_record(self):
        """
        Check for boot profiles that should be recorded. Copies raw data to hotstorage and marks profiles as recorded
        in config database.
        """
        self._get_boot_profiles()

    def _get_boot_profiles(self):
        boot_profiles = self._openData.get_boot_profiles()
        if boot_profiles is not None:
            boot_profiles_to_record = list(filter(lambda x: x.recorded is False, boot_profiles))
            for boot_profile in boot_profiles_to_record:
                for meter in boot_profile.meters:
                    try:
                        if "." in boot_profile.startTime:
                            start_time = boot_profile.startTime.split(".")[0] + "Z"
                        else:
                            start_time = boot_profile.startTime

                        start_date = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%SZ')
                        start_date = start_date.replace(tzinfo=get_localzone())
                        end_date = start_date + timedelta(hours=1)
                        local_time_now = datetime.now(get_localzone())
                        if local_time_now > end_date:
                            query = NpoeQueryHelper.get_boot_profile_query(start_date, end_date, meter.systemName,
                                                                           boot_profile.id)
                            df = self._clickhouse_client.get(query)
                            data = []
                            for i, row in df.iterrows():
                                variables = [row.Meter, row.MeasureTime.strftime("%Y-%m-%dT%H:%M:%S"),
                                             row.MeasureTimeUtc.strftime("%Y-%m-%dT%H:%M:%S"), row.Pt,
                                             row.ProfileId]
                                data.append(variables)

                            if len(data) > 0:
                                self._broker.send_message(topic="dataflow.fct.clickhouse",
                                                          key="sdk npoe",
                                                          data=[
                                                              HotStorageValue(table_name="npoe.boot_profiles_recorded",
                                                                              data=data).__dict__]
                                                          )
                                self._openData.set_boot_profiles_as_recorded([boot_profile.id])
                    except Exception:
                        print("Error - Boot profile recording error")
                        return None

    def get_organization_co2(self, organization_id: str) -> Optional[DataFrame]:
        """
        Gets Dates and Values of CO2 coefficients for specific organization

        Args:
            organization_id: (str) organization_id,

        Returns:
            DataFrame: Dates and Values of CO2 coefficient for selected organization
        """
        try:
            columns_to_validate = {'organization_id': organization_id}
            columns_info = OrganizationCo2DataValidator(**columns_to_validate)
            return self._get_organization_co2(organization_id=columns_info.organization_id)
        except Exception:
            print("Error = get organization values of co2 coefficients")
            return None

    def _get_organization_co2(self, organization_id) -> Optional[DataFrame]:
        """
        Gets Dates and Values of CO2 coefficients for specific organization with sql query

        Args:
            organization_id: (str) organization_id,

        Returns:
            DataFrame: Dates and Values of CO2 coefficient for selected organization
        """
        try:
            query = Query() \
                .SELECT("Date, Value") \
                .FROM(f"npoe.db_co2_coefficients") \
                .WHERE(f"OrganizationId = '{organization_id}'")
            print(query)
            df = self._clickhouse_client.get(query).sort_values('Date').reset_index(drop=True)
            print(df)
            return df
        except Exception:
            raise ValueError(f"Error = get organization values of co2 coefficients")

    def get_oze_connection_inverters(self, connection_id: str) -> Optional[DataFrame]:
        """
        Gets inverter SystemName for specific connection

        Args:
            connection_id: (str) connection_id,

        Returns:
            DataFrame: SystemNames of inverters for specific connection
        """
        try:
            columns_to_validate = {'connection_id': connection_id}
            columns_info = OzeConnectionInvertersDataValidator(**columns_to_validate)
            return self._get_oze_connection_inverters(connection_id=columns_info.connection_id)
        except Exception:
            print("Error = SystemNames of inverters for specific connection")
            return None

    def _get_oze_connection_inverters(self, connection_id) -> Optional[DataFrame]:
        """
        Gets inverter SystemName for specific connection with sql query

        Args:
            connection_id: (str) connection_id,

        Returns:
            DataFrame: SystemNames of inverters for specific connection
        """
        try:
            query = Query() \
                .SELECT("DISTINCT (SystemName)") \
                .FROM(f"npoe.inverters_agg_hour") \
                .WHERE(f"SystemName in (Select SystemName from npoe.db_producers dp WHERE "
                       f"ConnectionId = '{connection_id}')")

            df = self._clickhouse_client.get(query)
            return df
        except Exception:
            raise ValueError(f"Error = SystemNames of inverters for specific connection")

    def get_oze_connections_for_meters(self, meters: list) -> Optional[DataFrame]:
        """
        Gets meter SystemName for specific connection which has oze

        Args:
            meters: (list) meters,

        Returns:
            DataFrame: SystemName of meter for specific Connection which has oze
        """
        try:
            columns_to_validate = {'meters': meters}
            columns_info = OzeConnectionsForMetersDataValidator(**columns_to_validate)
            return self._get_oze_connections_for_meters(meters=columns_info.meters)
        except Exception:
            print("Error = SystemNames of meters for specific connection which has oze")
            return None

    def _get_oze_connections_for_meters(self, meters) -> Optional[DataFrame]:
        """
        Gets meter SystemName for specific connection which has oze with sql query

        Args:
            meters: (list) meters,

        Returns:
            DataFrame: SystemName of meter for specific Connection which has oze
        """
        try:
            meters_param = "','".join(meters)
            query = Query() \
                .SELECT("SystemName, ConnectionId") \
                .FROM(f"npoe.db_meters") \
                .WHERE(f"SystemName in('{meters_param}') and ConnectionId in (SELECT DISTINCT ConnectionId "
                       f"from npoe.db_producers dp)")
            df = self._clickhouse_client.get(query)
            return df
        except Exception:
            raise ValueError(f"Error = SystemNames of meters for specific connection which has oze")

    def get_inverters_summary_data(self, inverters: list, from_date: str, to_date: str) -> Optional[DataFrame]:
        """
        Gets time, produced and given energy from oze for specific SystemNames (inverters)

        Args:
            inverters: (list) inverters,
            from_date: (str) beginning of the time range
            to_date: (str) ending of the time range

        Returns:
            DataFrame: time, produced and given energy from oze for specific SystemNames (inverters)
        """
        try:
            columns_to_validate = {'inverters': inverters, 'from_date': from_date, 'to_date': to_date}
            columns_info = OzeInvertersSummaryDataValidator(**columns_to_validate)
            return self._get_inverters_summary_data(inverters=columns_info.inverters, from_date=columns_info.from_date,
                                                    to_date=columns_info.to_date)
        except Exception:
            print("Error = SystemNames of meters for specific connection which has oze")
            return None

    def _get_inverters_summary_data(self, inverters: list, from_date: str, to_date: str) -> Optional[DataFrame]:
        """
        Gets time, produced and given energy from oze for specific SystemNames (inverters) with sql query

        Args:
            inverters: (list) inverters,
            from_date: (str) beginning of the time range
            to_date: (str) ending of the time range

        Returns:
            DataFrame: time, produced and given energy from oze for specific SystemNames (inverters)
        """
        try:
            inverters_param = "','".join(inverters)
            query = Query() \
                .SELECT("MeasureTimeUtc, sum(I_Ac_Energy_Wh_Diff) as produced, sum(Ea_minus_Diff) as given") \
                .FROM(f"npoe.inverters_agg_hour") \
                .WHERE(f"SystemName IN ('{inverters_param}') AND MeasureTimeUtc >= '{from_date}' AND MeasureTimeUtc < "
                       f"'{to_date}' GROUP BY MeasureTimeUtc ORDER BY MeasureTimeUtc")
            print("Query:", query)
            df = self._clickhouse_client.get(query)
            return df
        except Exception:
            raise ValueError(f"Error = SystemNames of meters for specific connection which has oze")

    def get_meters_data(self, meters: list, from_date: str, to_date: str) -> Optional[DataFrame]:
        """
        Gets hourly energy consumption for specific SystemNames

        Args:
            meters: (list) meters,
            from_date: (str) beginning of the time range
            to_date: (str) ending of the time range

        Returns:
            DataFrame: hourly energy consumption for specific SystemNames
        """
        try:
            columns_to_validate = {'meters': meters, 'from_date': from_date, 'to_date': to_date}
            columns_info = MetersDataValidator(**columns_to_validate)
            return self._get_meters_data(meters=columns_info.meters, from_date=columns_info.from_date,
                                         to_date=columns_info.to_date)
        except Exception:
            print("Error = Energy consumption for specific SystemNames")
            return None

    def _get_meters_data(self, meters: list, from_date: str, to_date: str) -> Optional[DataFrame]:
        """
        Gets hourly energy consumption for specific SystemNames with sql query

        Args:
            meters: (list) meters,
            from_date: (str) beginning of the time range
            to_date: (str) ending of the time range

        Returns:
            DataFrame: hourly energy consumption for specific SystemNames
        """
        try:
            meters_param = "','".join(meters)
            query = Query() \
                .SELECT("MeasureTimeUtc,SystemName,Ea_Diff") \
                .FROM(f"npoe.electric_meters_agg_hour") \
                .WHERE(f"MeasureTimeUtc >= '{from_date}' AND MeasureTimeUtc < '{to_date}' AND SystemName IN "
                       f"('{meters_param}') order by MeasureTimeUtc")
            df = self._clickhouse_client.get(query)
            return df
        except Exception:
            raise ValueError(f"Error = Energy consumption for specific SystemNames")

    def get_connections(self) -> Optional[List[Connections]]:
        """
        Gets connections with meters for all organizations

        Returns:
            DataFrame: list of connections

        """

        try:
            df = self._openData.get_connections()
            return df
        except ValueError:
            print("Error - Get connections")
            return None
