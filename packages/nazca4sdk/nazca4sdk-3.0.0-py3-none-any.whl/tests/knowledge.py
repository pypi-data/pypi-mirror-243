from nazca4sdk.datahandling.knowledge.knowledge_data_type import KnowledgeDataType
from nazca4sdk.sdk import SDK
from nazca4sdk import FormatChart, FormatText
import requests
import datetime


sdk = SDK()
# odczyt dla danego klucza

# delete knowledge
sdk.knowledge.write_key_values("pomidor1", "sekcja pomidor1", "test", KnowledgeDataType.TEXT)
sdk.knowledge.write_key_values("pomidor1", "sekcja pomidor2", "test", KnowledgeDataType.TEXT)
sdk.knowledge.write_key_values("pomidor1", "sekcja pomidor3", "test", KnowledgeDataType.TEXT)

result = sdk.knowledge.delete_sections(["sekcja pomidor1", "sekcja pomidor2"], "pomidor1")

result3 = sdk.knowledge.write_key_values("pomidor1", "sekcja pomidor", "test", KnowledgeDataType.TEXT)
result2 = sdk.knowledge.write_key_values("pomidor2", "sekcja pomidor", "test", KnowledgeDataType.TEXT)
deleted_documents = sdk.knowledge.delete_keys(["pomidor1", "pomidor2"])

values = sdk.knowledge.read_keys("test")
keys = sdk.knowledge.read_keys("test", "2023-01-01T00:00:00", "2023-01-11T00:00:00", "0")
keys2 = sdk.knowledge.read_keys("test", "2023-01-01T00:00:00")
keys3 = sdk.knowledge.read_keys("test")
keys4 = sdk.knowledge.read_keys(size=4)
# print(values)

# result = sdk.write_knowledge("blob", "pliczek", "/2022-07-07_14-31.png", KnowledgeDataType.BLOB)
# result = sdk.write_knowledge("gruby", "sekcjaGruby", "test", KnowledgeDataType.TEXT)
# print(result)
