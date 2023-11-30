from nazca4sdk import SDK

sdk = SDK(False)

test = sdk.npoe.check_boot_profiles_to_record()
connections = sdk.npoe.get_connections()

# # get electric meters data
# electric_meters1 = sdk.npoe.get_electric_meters_data(system_name=["apa260"], time_amount=10, time_unit="HOUR")
# electric_meters2 = sdk.npoe.get_electric_meters_data(system_name=["apa260"],
#                                                      start_date='2023-08-07T00:00:00',
#                                                      end_date='2023-08-08T00:00:00')
# electric_meters3 = sdk.npoe.get_electric_meters_data(system_name=["apa260"],
#                                                      time_amount=10,
#                                                      time_unit="HOUR",
#                                                      variables=["U1", "U2"])
# print("electric_meters1: ", electric_meters1.head(2))
# print("electric_meters2: ", electric_meters2.head(2))
# print("electric_meters3: ", electric_meters3.head(2))

pg_max = sdk.npoe.calculate_pt_max_window()


pgavg_data = sdk.npoe.get_pgavg_data(connection="p_apa260",
                                     start_date='2023-08-07T00:00:00.345Z',
                                     end_date='2023-08-31T00:00:00.000Z')
print("pgavg: \n\n", pgavg_data.head(2))

sop_ssv_op_data = sdk.npoe.get_ssv_sop_orderedpower("p_apa260")
print("sop_ssv_op_data: \n\n", sop_ssv_op_data.head())

occ = sdk.analytics.energy.calculate_optimal_contracted_capacity(start_date='2023-08-01T00:00:00.398Z',
                                                                 end_date='2023-08-31T00:00:00.000Z',
                                                                 connection='p_apa260', simulated_ordered_power=20,
                                                                 ordered=False, simulated=True)
print(occ)