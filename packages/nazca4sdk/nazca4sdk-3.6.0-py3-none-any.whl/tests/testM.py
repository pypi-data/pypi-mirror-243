from nazca4sdk.sdk import SDK

sdk = SDK(False)
print(sdk.variables.read('symulator', ['V1'], time_unit='HOUR', time_amount=5))

print(sdk.variables.pivot('symulator', ['V1', 'V2'], time_unit='HOUR', time_amount=5))
