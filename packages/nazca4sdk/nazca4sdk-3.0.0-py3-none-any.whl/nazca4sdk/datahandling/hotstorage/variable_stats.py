from pydantic import BaseModel, StrictStr, validator
from typing import List


class VariableStats(BaseModel):
    module: str
    variable: str
    min: float
    max: float
    avg: float
    lastValue: float
    variance: float
    std: float


class VariablesStats(BaseModel):
    __root__: List[VariableStats]

    def stats(self):
        return self.__root__
