"""Module to calculate KPIs"""
from pandas import DataFrame
import pandas as pd
import numpy as np
from pydantic import ValidationError
from nazca4sdk.analytics.performance_indicators.oee_calculations import Oee
from nazca4sdk.analytics.performance_indicators.process_indicators import ProcessIndicators


class Indicators:
    """
    Indicators module with key performance indicators functions
    """

    def __init__(self):
        self.oee = Oee()
        self.process_indicators = ProcessIndicators()

    def get_oee_simple(self, availability: float, performance: float, quality: float):
        """The Overall Equipment Effectiveness (OEE)

        The Overall Equipment Effectiveness (OEE) is a proven way to monitor
        and improve process efficiency.
        it is considered as a diagnostic tool since it does not provide a solution to a given problem.
        OEE is a key process indicator that measures effectiveness and deviations
        from effective machine performance.

        OEE is calculated as:
            OEE = Availability x Performance x Quality
        Args:
            availability: float
            performance: float
            quality: float

        Return:
            OEE value: float

        Example:
            get_oee_simple(availability: 50, performance: 30, quality: 60)
        """
        try:
            data = {"availability": availability,
                    "performance": performance,
                    "quality": quality
                    }
            result = self.oee.calculate_oee_simple(data)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_oee_complex(self, a: float, b: float, c: float, d: float, e: float, f: float):
        """The Overall Equipment Effectiveness (OEE)

        The Overall Equipment Effectiveness (OEE) is a proven way to monitor
        and improve process efficiency.
        it is considered as a diagnostic tool since it does not provide a solution to a given problem.
        OEE is a key process indicator that measures effectiveness and deviations
        from effective machine performance.

        Args:
        OEE depends on parameters as follows:
            A = Total available time
            B = Run time
            C = Production capacity
            D = Actual production
            E = Production output (same as actual production)
            F = Actual good products (i.e. product output minus scraps)
        where,
        A and B define Availability,
        C and D define Performance,
        E and F define Quality

        OEE is calculated as:

        OEE = (B/A) x (D/C) x (F/E)

        Returns:
            OEE value: float

        Example:
            get_oee_complex(A: 50, B: 40, C: 60, D: 20, E: 100, F: 10)
        """
        try:
            data = {"A": a,
                    "B": b,
                    "C": c,
                    "D": d,
                    "E": e,
                    "F": f
                    }
            result = self.oee.calculate_oee_complete(data)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_availability(self, run_time: float, total_time: float):
        """Availability

            Takes into account availability/time loss, which includes all events
            related to unplanned stops.
            (e.g. equipment failures, material shortages) and planned stops (e.g. changeover times).
            Availability measures the proportion of time a machine or cell runs
            from the total theoretical available time.
            Calculated as:
                Availability = Run time/Total available time
            Args:
                ::input -> dictionary with oee parameters::
                run_time, Run time in hours
                total_time, Total run time in hours

            Returns:
                availability value: float

            Example:
                get_availability(run_time: 30, total_time: 50)
            """
        try:
            data = {"run_time": run_time,
                    "total_time": total_time,
                    }
            result = self.oee.calculate_availability(data)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_performance(self, actual_production: float, production_capacity: float):
        """Performance

            Takes into account performance/speed loss, which includes all the factors
            (e.g. slow cycles, small stops)
            that prevent the machine or cell to operate at maximum/optimal speed.
            It measures the proportion of produced units from the total number of possible
            produced units in a given run.

            Calculated as:
                Performance = Actual production/Production capacity

            Args:
                ::performance_input -> dictionary with performance parameters::
                actual_production, actual production
                production_capacity, production capacity

            Returns:
                performance value: float

            Example:
                get_performance(actual_production: 30, production_capacity: 50)
            """
        try:
            data = {"actual_production": actual_production,
                    "production_capacity": production_capacity,
                    }
            result = self.oee.calculate_availability(data)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_quality(self, actual_products: float, production_output: float):
        """Quality

            Takes into account quality loss, which includes all the factors
            (e.g. reworks, scraps, defects).
            that lead to defective units that do not meet the customer’s quality
            standards and specifications.
            Quality measures the proportion of non-defective units compared
            to the total units produced.
            Calculated as:
                Quality = Actual good products/Product output
            Args:
                ::quality_input -> dictionary with performance parameters::
                actual_products, Actual good products
                production_output, Production output

            Returns:
                quality value: float

            Example:
                get_quality(actual_products: 30, production_output: 50)
            """
        try:
            data = {"actual_products": actual_products,
                    "production_output": production_output,
                    }
            result = self.oee.calculate_quality(data)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_cp_indicator(self, module: str, variable: str, start_date: str, end_date: str, period: int, subgroups: int, estimation_type='samples', **limits: dict):
        """
        The function to calculate Process Capability Indicator (Cp)

        Args:
            module: module name,
            variable: variable name,
            start_date: start of date range,
            end_date: end of date range,
            period: when estimation_type = 'samples', this is number of samples,
                for estimation_type = 'time' this is number of seconds
            subgroups: number of samples in subgroups,
            estimation_type: 'time' to estimate std using time offset or 'samples'
            to estimate using number of samples offset,
            limits: lsl, usl or both

        Return:
            Cp value

        """
        try:

            data = {"module": module,
                    "variable": variable,
                    "start_date": start_date,
                    "end_date": end_date,
                    "period": period,
                    "subgroups": subgroups,
                    "estimation_type": estimation_type
                    }
            keys = limits.keys()
            if "lsl" in keys and "usl" in keys:
                data['lsl'] = limits.get("lsl")
                data['usl'] = limits.get("usl")
            elif "lsl" in keys:
                data['lsl'] = limits.get("lsl")
            elif "usl" in keys:
                data['usl'] = limits.get("usl")

            result = self.process_indicators.get_cp_indicator(data)
            if result is None:
                return None
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_pp_indicator(self, module: str, variable: str, start_date: str, end_date: str, **limits: dict):
        """
        The function to calculate Process Performance Indicator (Pp)

        Args:
            module: module name,
            variable: variable name,
            start_date: start of date range,
            end_date: end of date range,
            limits: lsl, usl or both

        Return:
            Pp value

        """
        try:
            data = {"module": module,
                    "variable": variable,
                    "start_date": start_date,
                    "end_date": end_date,
                    }
            keys = limits.keys()
            if "lsl" in keys and "usl" in keys:
                data['lsl'] = limits.get("lsl")
                data['usl'] = limits.get("usl")
            elif "lsl" in keys:
                data['lsl'] = limits.get("lsl")
            elif "usl" in keys:
                data['usl'] = limits.get("usl")

            result = self.process_indicators.get_pp_indicator(data)
            if result is None:
                return None
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_cpk_indicator(self, module: str, variable: str, start_date: str, end_date: str, period: float, subgroups: int, estimation_type='samples', **limits: dict):
        """
        The function to calculate Process Capability Index (Cpk)

        Args:
            module: module name,
            variable: variable name,
            start_date: start of date range,
            end_date: end of date range,
            period: number of samples between subgroups,
            subgroups: number of samples in subgroups,
            estimation_type: 'time' to estimate std using time offset or 'samples'
            to estimate using number of samples offset,
            limits: lsl, usl or both

        Return:
            Cpk value: float
        """
        try:

            data = {"module": module,
                    "variable": variable,
                    "start_date": start_date,
                    "end_date": end_date,
                    "period": period,
                    "subgroups": subgroups,
                    "estimation_type": estimation_type
                    }

            keys = limits.keys()
            if "lsl" in keys and "usl" in keys:
                data['lsl'] = limits.get("lsl")
                data['usl'] = limits.get("usl")
            elif "lsl" in keys:
                data['lsl'] = limits.get("lsl")
            elif "usl" in keys:
                data['usl'] = limits.get("usl")
            result = self.process_indicators.get_cpk_indicator(data)
            if result is None:
                return None
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_ppk_indicator(self, module: str, variable: str, start_date: str, end_date: str, **limits: dict):
        """
        The function to calculate Process Performance Index (Ppk)

        Args:
            module: module name,
            variable: variable name,
            start_date: start of date range,
            end_date: end of date range,
            limits: lsl, usl or both

        Return:
            Ppk value

        """
        try:
            data = {"module": module,
                    "variable": variable,
                    "start_date": start_date,
                    "end_date": end_date,
                    }
            keys = limits.keys()
            if "lsl" in keys and "usl" in keys:
                data['lsl'] = limits.get("lsl")
                data['usl'] = limits.get("usl")
            elif "lsl" in keys:
                data['lsl'] = limits.get("lsl")
            elif "usl" in keys:
                data['usl'] = limits.get("usl")

            result = self.process_indicators.get_ppk_indicator(data)
            if result is None:
                return None
            return result
        except ValidationError as error:
            print(error.json())
            return None
