from typing import List
from pydantic import BaseModel, StrictStr


class NazcaVariable(BaseModel):
    identifier: StrictStr
    description: StrictStr
    id: int
    value: object
    valueType: StrictStr


class NazcaVariables(BaseModel):
    __root__: List[NazcaVariable]

    def variables(self):
        return self.__root__
