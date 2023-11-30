from nazca4sdk.sdk import SDK


sdk = SDK(False)
# print(sdk.analytics.kpi.get_pp_indicator('symulator', 'V1',
#       '2023-03-21T11:50:00', '2023-03-21T11:55:00', usl=220))

print(sdk.analytics.kpi.get_cpk_indicator('symulator', 'V1',
      '2023-03-21T11:50:00', '2023-03-21T11:55:00', 10, 3, 'time', lsl=220, usl=240))
