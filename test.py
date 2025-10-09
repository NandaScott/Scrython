import scrython

bulk_data = scrython.bulk_data.BulkData()
print(type(bulk_data), bulk_data.object)

bulk_data = scrython.bulk_data.BulkData(id='922288cb-4bef-45e1-bb30-0c2bd3d3534f')
print(type(bulk_data), bulk_data.type)

bulk_data = scrython.bulk_data.BulkData(type='oracle-cards')
print(type(bulk_data), bulk_data.type)
