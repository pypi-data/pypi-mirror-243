from nazca4sdk.datahandling.hotstorage.query import Query


class NpoeQueryHelper:
    @staticmethod
    def get_boot_profile_query(start_date, end_date, meter, profile_id):
        return Query() \
            .SELECT(f"SystemName as Meter,"
                    f"MeasureTime,"
                    f"MeasureTimeUtc,"
                    f"Pt,"
                    f"'{profile_id}' as ProfileId") \
            .FROM(f"npoe.electric_meters_raw emr") \
            .WHERE(f"MeasureTimeUtc >= '{start_date.strftime('%Y-%m-%dZ%H:%M:%S')}' "
                   f"AND "
                   f"MeasureTimeUtc < '{end_date.strftime('%Y-%m-%dZ%H:%M:%S')}' "
                   f"AND "
                   f"SystemName = '{meter}'")

    @staticmethod
    def get_pt_max_window_query(start_date, end_date):
        return Query() \
            .SELECT(f"pgams.Connection AS Connection, \
                                    toStartOfHour(pgams.MeasureTime) AS MeasureTime, \
                                    toStartOfHour(pgams.MeasureTimeUtc) AS MeasureTimeUtc, \
                                    last_value(pgams.Time_Inc) AS Time_Inc, \
                                    max(pgams.Pt_Avg_Sum) AS Pt_Window_Max") \
            .FROM(f"(SELECT \
                                        pgam.Connection AS Connection, \
                                        pgam.MeasureTime AS MeasureTime, \
                                        pgam.MeasureTimeUtc AS MeasureTimeUtc, \
                                        pgam.Time_Inc AS Time_Inc, \
                                        sum(Pt_Avg) AS Pt_Avg_Sum \
                                    FROM \
                                    ( \
                                        SELECT \
                                            db_connections.SystemName AS Connection, \
                                            db_meters.SystemName AS Meter, \
                                            toStartOfInterval(electric_meters_raw.MeasureTime,toIntervalMinute(15)) AS MeasureTime, \
                                            toStartOfInterval(electric_meters_raw.MeasureTimeUtc,toIntervalMinute(15)) AS MeasureTimeUtc, \
                                            last_value(electric_meters_raw.Time_Inc) AS Time_Inc, \
                                            avg(Pt) AS Pt_Avg \
                                        FROM npoe.electric_meters_raw AS electric_meters_raw \
                                        INNER JOIN npoe.db_meters AS db_meters ON electric_meters_raw.SystemName = db_meters.SystemName \
                                        INNER JOIN npoe.db_connections AS db_connections ON db_meters.ConnectionId = db_connections.Id \
                                        WHERE MeasureTimeUtc >= '{start_date.strftime('%Y-%m-%dT%H:%M:%S')}' \
                                        AND   MeasureTimeUtc < '{end_date.strftime('%Y-%m-%dT%H:%M:%S')}' \
                                        GROUP BY \
                                            Connection, \
                                            Meter, \
                                            MeasureTime, \
                                            MeasureTimeUtc \
                                        ORDER BY \
                                            Connection ASC, \
                                            Meter ASC, \
                                            MeasureTime ASC, \
                                            MeasureTimeUtc ASC \
                                    ) AS pgam \
                                    GROUP BY \
                                        Connection, \
                                        MeasureTime, \
                                        MeasureTimeUtc, \
                                        Time_Inc) as pgams"
                  ) \
            .GROUP_BY(f"Connection, MeasureTime, MeasureTimeUtc") \
            .ORDER_BY(f"Connection ASC, MeasureTime ASC, MeasureTimeUtc ASC")
