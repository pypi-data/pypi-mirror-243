from datetime import datetime
from pydantic import BaseModel, validator

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_TIME_EXAMPLE = "yyyy-mm-ddTHH:MM:SS"

class VariableStatsInfo(BaseModel):
    module : str
    variables = {}
    startDate: str
    endDate: str

    @validator("endDate")
    def validate_end_date(cls, valid_datetime):
        """Validator to check if time amount is correct

               Args:
                   valid_datetime: str

               Returns:
                   valid_datetime: str
               """
        try:
            datetime.strptime(valid_datetime, DATE_TIME_FORMAT)
            return valid_datetime
        except ValueError:
            raise ValueError(
                f'Bad datetime format. Example {DATE_TIME_EXAMPLE} ')

    @validator("startDate")
    def valid_start_date(cls, valid_datetime):
        """Validator to check if time amount is correct

        Args:
            valid_datetime: str

        Returns:
            valid_datetime: str
        """
        try:
            datetime.strptime(valid_datetime, DATE_TIME_FORMAT)
            return valid_datetime
        except ValueError:
            raise ValueError(
                f'Bad datetime format. Example {DATE_TIME_EXAMPLE}')