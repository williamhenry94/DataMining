from pymongo import MongoClient

from shapely.wkt import loads
from geojson import Feature

client = MongoClient("ds013495.mlab.com",13495) # 
db = client.crime_database
db.authenticate('root','root')


collection = db.Brisbane_East.find({"geoJson":{"$exists":False}})
print (collection.count())
for i in collection:
    # if "GeometryWKT" in i:
    print (i["MeshBlockId"])
    geoJ = Feature(geometry =loads(i["GeometryWKT"]),properties={})

    db.Brisbane_East.update({"MeshBlockId":i["MeshBlockId"]}, {"$set":{"geoJson":geoJ}})