from typing import List
from pydantic import BaseModel
from nazca4sdk.datahandling.npoe.meter import Meter


class Connection(BaseModel):
    systemName: str
    organizationId: str
    id: str
    orderedPower: int
    meters: List[Meter]


class Connections(BaseModel):
    __root__: List[Connection]

    def connections(self):
        return self.__root__
