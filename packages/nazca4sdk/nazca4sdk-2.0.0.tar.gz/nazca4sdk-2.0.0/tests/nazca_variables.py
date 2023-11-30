from nazca4sdk import SDK

sdk = SDK(False)
print(sdk.nazca_variables.read())

# value = sdk.read_nazca_variable("double")
# print(value)
