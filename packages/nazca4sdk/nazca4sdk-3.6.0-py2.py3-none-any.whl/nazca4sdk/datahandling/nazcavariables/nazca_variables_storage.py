from nazca4sdk.datahandling.nazcavariables.nazca_variable import NazcaVariables, NazcaVariable
from nazca4sdk.datahandling.open_data_client import OpenDataClient
from dependency_injector.wiring import inject


class NazcaVariablesStorage:

    @inject
    def __init__(self,  opendata_client: OpenDataClient):
        self._opendata = opendata_client

    def read(self, name: str = None):
        """Read nazca variables

            Args:
                name: name of variable, if None return all variables
            Returns:
                if name == None return all nazca variables
                if name set then return nazca variable with specified name
        """

        if name is None:
            return self._read_variables()
        else:
            return self._read_variable(name)

    def _read_variables(self):
        """  Read all nazca variables

              Returns:
                  all nazca variables
        """
        response = self._opendata.read_nazca_variables()
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("Read nazca variable failure")
                return None
            variables_list = NazcaVariables.parse_raw(response.content)
            return variables_list.variables()
        print("Read nazca variables error")
        return None

    def _read_variable(self, identifier: str):
        """ Read nazca variable with identifier

                Args:
                    identifier: nazca variable identifier
                Returns:
                    nazca variable
        """

        response = self._opendata.read_nazca_variable(identifier)
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("Read nazca variable failure")
                return None
            variable = NazcaVariable.parse_raw(response.content)
            return variable
        if response.status_code == 404:
            print(f"Nazca variable {identifier} not found")
            return None
        print(f"Read nazca variable {identifier} error")
        return None
