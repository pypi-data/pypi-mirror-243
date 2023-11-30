"""Module for forecasting"""
from nazca4sdk.analytics.prediction.predictions import Predictions, forecast_prediction
from nazca4sdk.datahandling.variable_verificator import VariableIntervalSubtractionInfo, VariableType, \
    ForecastForPrediction
from nazca4sdk.system.system_cache import SystemCache
from pydantic import ValidationError


class Forecasting:
    """
    Forecasting module with functions for forecasting
    """

    def __init__(self, cache: SystemCache):
        self._system_cache = cache

    def predict(self, module_name: str, variable_names: str, time_amount: int, time_unit: str,
                forecast_time_amount: int, forecast_time_unit: str, prediction_tool: str = "prophet"):
        """
        Predict value for the future based on prophet procedure

        Args:
            module_name: name of module,
            variable_names: list of variable names,
            time_amount: beginning of the time range
            time_unit: 'DAY','HOUR'...
            forecast_time_amount: int: periods forecast: 10,50,60
            forecast_time_unit: str: frequency for forecast time: '1min', '5min'...
            prediction_tool: str: "prophet" or "nixtla"

        Returns:
            result dict with:
                lower_bound, upper_bound, prediction value, mse error, mae errors
        """

        try:
            exist = self._system_cache.check_if_exist(module_name, [variable_names])
            if not exist:
                print(f"Module {module_name} or {variable_names} not exist")
                return None
            variables_group = self._system_cache.group_variables(module_name, [variable_names])
            variables_grouped = {'variables_grouped': variables_group}
            variable = VariableType(**variables_grouped).variable_verify_type(variables_group)

            input_data = {
                "module_name": module_name,
                "variable_names": [variable],
                "time_amount": time_amount,
                "time_unit": time_unit
            }
            data_input = dict(
                VariableIntervalSubtractionInfo(**{"time_amount": time_amount,
                                                   "time_unit": time_unit
                                                   }))

            input_forecast = {
                "forecast_time_amount": forecast_time_amount,
                "forecast_time_unit": forecast_time_unit,
                "prediction_tool": prediction_tool
            }

            data_forecast = dict(ForecastForPrediction(**input_forecast))

            result = forecast_prediction(Predictions(input_data['module_name'], input_data['variable_names'][0],
                                                     data_input['time_amount'], data_input['time_unit'],
                                                     data_forecast['forecast_time_amount'],
                                                     data_forecast['forecast_time_unit'],
                                                     data_forecast['prediction_tool']))
            return result

        except ValidationError as error:
            print(error.json())
            return None
