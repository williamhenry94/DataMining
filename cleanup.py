from pymongo import MongoClient
from pprint import pprint
client = MongoClient('localhost',27017)
db = client.DataMining

collection = db.Brisbane_South
collection2 = db.Brisbane_South_new

dataset = collection2.find({})

offenceIds = []

for i in dataset:
    # print ("MeshBlockId: ",i["MeshBlockId"])
    
    temp = []
    for ii in i["OffenceInfo"]:
        if ii["QpsOffenceId"] not in offenceIds:
            offenceIds.append(ii["QpsOffenceId"])
            temp.append(ii)
        else:
            print ("detected duplicate: ", ii["QpsOffenceId"])
    
    newData = {"MeshBlockId":i["MeshBlockId"], "GeometryWKT":i["GeometryWKT"],"GeometryWKID":i["GeometryWKID"],"OffenceInfo":temp}
    # collection2.insert(newData)



