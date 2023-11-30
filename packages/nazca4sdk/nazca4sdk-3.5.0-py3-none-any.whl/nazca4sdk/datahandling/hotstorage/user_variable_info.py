from dataclasses import dataclass
from nazca4sdk.datahandling.hotstorage.model.user_variable import UserVariableDataType


@dataclass()
class UserVariableInfo:
    type: UserVariableDataType
    name: str
