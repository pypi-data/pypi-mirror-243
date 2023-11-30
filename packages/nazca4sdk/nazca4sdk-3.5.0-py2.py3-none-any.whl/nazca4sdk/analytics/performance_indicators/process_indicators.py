"""Module to calculate process indicators"""
from pydantic import ValidationError
from nazca4sdk.analytics.__brain_connection import BrainClient
from nazca4sdk.datahandling.variable_verificator import CpCpkIndicatorsParams, PpPpkIndicatorsParams


class ProcessIndicators:
    """ Class to perform process indicators calculation with cooperation with Brain """

    def __init__(self):
        self.indicators_brain = BrainClient()

    def get_cp_indicator(self, cp_input: dict):
        """
        Function to determine Cp indicator values for determined input

        Args:
            cp_input: dictionary with input parameters

        Returns:
            Cp indicator

       """

        try:
            data = dict(CpCpkIndicatorsParams(**cp_input))
            response = self.indicators_brain.get_cp_indicator(data)
            result = self.indicators_brain.parse_response(response)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_pp_indicator(self, pp_input: dict):
        """
        Function to determine Pp indicator values for determined input

        Args:
            pp_input: dictionary with input parameters

        Returns:
            Pp indicator

       """

        try:
            data = dict(PpPpkIndicatorsParams(**pp_input))
            response = self.indicators_brain.get_pp_indicator(data)
            result = self.indicators_brain.parse_response(response)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_cpk_indicator(self, cpk_input: dict):
        """
        Function to determine Cpk indicator values for determined input

        Args:
            cpk_input: dictionary with input parameters

        Returns:
            Cpk indicator

        """

        try:
            data = dict(CpCpkIndicatorsParams(**cpk_input))
            response = self.indicators_brain.get_cpk_indicator(data)
            result = self.indicators_brain.parse_response(response)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def get_ppk_indicator(self, ppk_input: dict):
        """
        Function to determine Ppk indicator values for determined input

        Args:
            ppk_input: dictionary with input parameters

        Returns:
            Ppk indicator

        """

        try:
            data = dict(PpPpkIndicatorsParams(**ppk_input))
            response = self.indicators_brain.get_ppk_indicator(data)
            result = self.indicators_brain.parse_response(response)
            return result
        except ValidationError as error:
            print(error.json())
            return None
