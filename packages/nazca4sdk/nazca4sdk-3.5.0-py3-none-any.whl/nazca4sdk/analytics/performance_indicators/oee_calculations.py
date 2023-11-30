"""Module to calculate OEE"""
from pydantic import ValidationError
from nazca4sdk.analytics.__brain_connection import BrainClient
from nazca4sdk.datahandling.variable_verificator import OeeSimpleParams, OeeComplexParams, \
    AvailabilityValidator, PerformanceValidator, QualityValidator


class Oee:
    """ Class to perform Oee calculation with cooperation with Brain """

    def __init__(self):
        self.oee_brain = BrainClient()

    def calculate_oee_simple(self, simple_input: dict):
        """
        Function to determine energy quality values for determined input

        Args:
        simple_input -> dictionary with simple oee parameters:
            availability: (float) proces availability,
            performance: (float) proces performance,
            quality: (float) proces quality

        Returns:
            oee parameter: float
       """

        try:
            data = dict(OeeSimpleParams(**simple_input))
            response = self.oee_brain.get_oee_easy(data)
            result = self.oee_brain.parse_response(response)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    def calculate_oee_complete(self, complex_input: dict):
        """
        Function to determine energy quality values for determined input

            Args:
            complex_input -> dictionary with complex oee parameters::
                availability,
                performance,
                quality

        Returns:
            float: oee parameter
        """

        try:
            data = dict(OeeComplexParams(**complex_input))
            response = self.oee_brain.get_oee_full(data)
            result = self.oee_brain.parse_response(response)
            return result
        except ValidationError as error:
            print(error.json())
            return None

    @staticmethod
    def calculate_availability(availability_input: dict):
        """
        Availability:
        Takes into account availability/time loss, which includes all events
        related to unplanned stops
        (e.g. equipment failures, material shortages) and planned stops
        (e.g. changeover times).
        Availability measures the proportion of time a machine or cell runs from
        the total theoretical available time.

        Calculated as:

        Availability = Run time/Total available time
        Args:
            ::availability_input -> dictionary with availability parameters::
            run_time,
            total_time,

        Returns:
            Availability value: float
        """

        try:
            data = AvailabilityValidator(**availability_input)
            result = data.run_time / data.total_time
            return result
        except ValidationError as error:
            print(error.json())
            return None

    @staticmethod
    def calculate_performance(performance_input: dict):
        """Performance:Takes into account performance/speed loss,
        which includes all the factors
        (e.g. slow cycles, small steps)
        that prevent the machine or cell to operate at maximum/optimal speed.
        It measures the proportion of produced units from the total number of
        possible produced units in a given run.

        Calculated as:

        Performance = Actual production/Production capacity

        Args:
        :performance_input -> dictionary with performance parameters:
            actual_production, Actual production
            production_capacity, Production capacity

        Returns:
            Performance value: float
        """

        try:
            data = PerformanceValidator(**performance_input)
            result = data.actual_production / data.production_capacity
            return result
        except ValidationError as error:
            print(error.json())
            return None

    @staticmethod
    def calculate_quality(quality_input: dict):
        """
        Quality:
        Takes into account quality loss, which includes all the factors
        (e.g. reworks, scraps, defects)
        that lead to defective units that do not meet the customer’s quality
        standards and specifications.
        Quality measures the proportion of non-defective units
        compared to the total units produced.

        Calculated as:

        Quality = Actual good products/Product output
        Args:
            :quality_input -> dictionary with performance parameters::
            actual_products, Actual good products
            production_output, Production output

        Returns:
            Quality valueL: float
        """

        try:
            data = QualityValidator(**quality_input)
            result = data.actual_products / data.production_output
            return result
        except ValidationError as error:
            print(error.json())
            return None
