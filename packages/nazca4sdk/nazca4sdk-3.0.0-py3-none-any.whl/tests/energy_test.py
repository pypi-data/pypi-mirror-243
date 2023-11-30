from nazca4sdk.sdk import SDK
#
# sdk = SDK(False)
#
# print(sdk.modules)

from nazca4sdk.datahandling.variable_verificator import EnergyInput, VibrationInput
#
# params = EnergyInput(freq1=50, vol1 = 230, cos1=1, thd1=0, freq2=50, vol2 = 230, cos2=1, thd2=0, freq3=50, vol3 = 230, cos3=1, thd3=0)
#
from nazca4sdk.analytics.energy.energy_quality import EnergyQuality
energy_quality = EnergyQuality()
print(energy_quality.calculate_energy_by_params(EnergyInput(freq1=50, vol1 = 230, cos1=1, thd1=0,
                                                            freq2=50, vol2 = 230, cos2=1, thd2=0,
                                                            freq3=50, vol3 = 230, cos3=1, thd3=0, standard=1)))
#
from nazca4sdk.datahandling.variable_verificator import VibrationInput
from nazca4sdk.analytics.vibration.vibration_quality import VibrationQuality
vibration_quality = VibrationQuality()
print(vibration_quality.calculate_vibration_quality_by_params(VibrationInput(group = 'G1r', vibration = 1)))

# print(energy_quality.calculate_energy_quality(module = 'symulator'))