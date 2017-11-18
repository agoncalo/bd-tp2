import pymongo

uri = "mongodb://tpbd:Pc48J1UiXZBn3xaumgBkxGrBHw00k9PCr0daNqRHnXoqXnv0nciTjxv85yWQo1X5rerrsbS0b3uDN0lMOy9nAA==@tpbd.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
client = pymongo.MongoClient(uri)

banco = client['tpdb']

import datetime


forum = {"author": "Thiago Avelino",  "text": "Python e MongoDB", "tags": ["mongodb", "python", "pymongo"]}
db = banco.teste


teste = db.teste
teste.insert(forum)

print(teste.find_one())