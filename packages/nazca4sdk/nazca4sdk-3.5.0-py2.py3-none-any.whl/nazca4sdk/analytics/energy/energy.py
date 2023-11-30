"""Module to calculate energy quality according to EN50160"""
import logging
from typing import Optional

from pydantic import ValidationError
from nazca4sdk.analytics.__brain_connection import BrainClient


class Energy:
    """ Class to send and receive information from Energy module in brain"""

    def __init__(self):
        self.energy_brain = BrainClient()

    def calculate_energy_quality(self, module: str, npoe: Optional[bool] = False):
        """
        Function to determine energy quality values for determined input

        Args:
            npoe: Optional: if data should be import from npoe
            module: module name
        Returns:
            ::energy quality parameters -> dictionary with energy quality parameters::
            (worstCaseQuality: Overall energy quality;
            worstCaseQuality1: Overall energy quality of phase 1;
            worstCaseQuality2 Overall energy quality of phase 2;
            worstCaseQuality3: Overall energy quality of phase 3;
            frequencyQuality1: Overall frequency quality of phase 1;
            voltageQuality1: Overall voltage quality of phase 1;
            cosQuality1: Overall cosinus quality of phase 1;
            thdQuality1: Overall thd quality of phase 1;
            frequencyQuality2: Overall frequency quality of phase 2;
            voltageQuality2: Overall voltage quality of phase 2;
            cosQuality2: Overall cosinus quality of phase 2;
            thdQuality2: Overall thd quality of phase 2;
            frequencyQuality3: Overall frequency quality of phase 3;
            voltageQuality3: Overall voltage quality of phase 3;
            cosQuality3: Overall cosinus quality of phase 3;
            thdQuality3: Overall thd quality of phase 3;
        """

        try:
            response = self.energy_brain.get_energy_quality(module, npoe)
            result = self.energy_brain.parse_response(response)
            logging.info(f'Response: {result}')
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def calculate_energy_by_params(self, **kwargs):
        """
        Function to calculate energy quality by params
        Args:
            standard: Optional(int)
            freq1: Optional(float) frequency value phase 1;
            vol1: Optional(float) voltage value phase 1;
            cos1: Optional(float) cosinous value phase 1;
            thd1: Optional(float) thd value phase 1;
            freq2: Optional(float) frequency value phase 2;
            vol2: Optional(float) voltage value phase 2;
            cos2: Optional(float) cosinus value phase 2;
            thd2: Optional(float) thd value phase 2;
            freq3: Optional(float) frequency value phase 3;
            vol3: Optional(float) voltage value phase 3;
            cos3: Optional(float) cosinus value phase 3;
            thd3: Optional(float) thd value phase 3;

        Returns:
            ::energy quality parameters -> dictionary with energy quality parameters::
            (worstCaseQuality: Overall energy quality;
            worstCaseQuality1: Overall energy quality of phase 1;
            worstCaseQuality2 Overall energy quality of phase 2;
            worstCaseQuality3: Overall energy quality of phase 3;
            frequencyQuality1: Overall frequency quality of phase 1;
            voltageQuality1: Overall voltage quality of phase 1;
            cosQuality1: Overall cosinus quality of phase 1;
            thdQuality1: Overall thd quality of phase 1;
            frequencyQuality2: Overall frequency quality of phase 2;
            voltageQuality2: Overall voltage quality of phase 2;
            cosQuality2: Overall cosinus quality of phase 2;
            thdQuality2: Overall thd quality of phase 2;
            frequencyQuality3: Overall frequency quality of phase 3;
            voltageQuality3: Overall voltage quality of phase 3;
            cosQuality3: Overall cosinus quality of phase 3;
            thdQuality3: Overall thd quality of phase 3;
        """

        try:
            for i in kwargs.keys():
                if i not in ["freq1", "vol1", "cos1", "thd1", "freq2", "vol2", "cos2", "thd2", "freq3", "vol3", "cos3",
                             "thd3", "standard"]:
                    return NameError('Energy parameters should contains these names: freq1, vol1, cos1, thd1, freq2,'
                                     'vol2, cos2, thd2, freq3, vol3, cos3, thd3, standard')
            response = self.energy_brain.get_energy_quality_by_params(dict(**kwargs))
            result = self.energy_brain.parse_response(response)
            logging.info(f'Response: {result}')
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def calculate_optimal_contracted_capacity(self, start_date: str, end_date: str, connection: str,
                                              simulated_ordered_power: int = 0,
                                              ordered: bool = False, simulated: bool = False):
        """
        Function to calculate optimal contracted capacity for determined input

        Args:
            start_date: start date in UTC
            end_date: start date in UTC
            connection:
            simulated_ordered_power: simulated power by user, or 0 if power should be read from database
            ordered: bool value, if power should be read from database or from user
            simulated: bool value, if algorithm should simulate return values with provided simulatedOrderedPower
        Returns:
            ::optimal contracted capacity -> dictionary with optimal contracted capacity parameters::
            fee,
            penalty,
            power,
            summary
        """
        try:
            response = self.energy_brain.get_optimal_contracted_capacity(start_date,
                                                                         end_date,
                                                                         connection,
                                                                         simulated_ordered_power,
                                                                         ordered,
                                                                         simulated)
            result = self.energy_brain.parse_response(response)
            logging.info(f'Response: {result}')
            return result
        except ValidationError as error:
            print(error.json())
            return None
