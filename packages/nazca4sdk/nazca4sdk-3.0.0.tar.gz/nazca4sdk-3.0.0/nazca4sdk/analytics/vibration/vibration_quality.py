"""Module to calculate vibration quality"""
import logging
from pydantic import ValidationError
from nazca4sdk.analytics.__brain_connection import BrainClient


class VibrationQuality:
    """ Class to send and receive information from Vibration quality module in brain"""

    def __init__(self):
        self.vibration_brain = BrainClient()

    def calculate_vibration_quality(self, group: str, module: str):
        """Function to determine vibration quality values for determined input

        Args:
            group: group name
            module: module name

        Returns:
            dict: vibration quality parameters
        """

        try:
            logging.info(f'Module Name: {module}, Group: {group}')
            response = self.vibration_brain.get_vibration_quality(group, module)
            result = self.vibration_brain.parse_response(response)
            logging.info(f'Response: {result}')
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def calculate_vibration_quality_by_params(self, group: str, vibration):
        """Function to determine vibration quality values for determined input

        Args:
            group: group name
            vibration: vibration value

        Returns:
            vibration quality parameters based on ISO norm
        """

        try:
            logging.info(f'Vibration: {vibration}, Group: {group}')

            if not isinstance(vibration, float):
                return TypeError(f'vibration is not a valid float, should be {float(vibration)}')
            response = self.vibration_brain.get_vibration_quality_by_params(group, vibration)
            result = self.vibration_brain.parse_response(response)
            logging.info(f'Response: {result}')
            return result
        except ValidationError as error:
            print(error.json())
            return None
