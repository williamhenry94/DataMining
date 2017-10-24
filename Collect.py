from InformationSummariser import getDatas
import json
from pymongo import MongoClient
import hashlib
def main(anticedent, consequent, support, confidence,lift):

    # client = MongoClient('localhost', 27017)
    # db = client.DataMiningSub

    client = MongoClient("ds013495.mlab.com",13495) # 
    db = client.crime_database
    db.authenticate('root','root')

    innerCollection = db.Inner_Suburbs
    southernCollection = db.Southern_Suburbs
    northernCollection = db.Northern_Suburbs
    easternCollection = db.Eastern_Suburbs
    westernCollection = db.Western_Suburbs

    with open('suburbs2.json') as f:
        suburbs = json.load(f)
    inner = suburbs["Brisbane_inner"]
    south = suburbs["Brisbane_south"]
    east = suburbs["Brisbane_east"]
    west = suburbs["Brisbane_west"]
    north = suburbs["Brisbane_north"]

    inner = [i.upper() for i in inner]
    south = [i.upper() for i in south]
    east = [i.upper() for i in east]
    west = [i.upper() for i in west]
    north = [i.upper() for i in north]


    d = getDatas(crime=anticedent["QpsOffence"], Solved=consequent["Solved"])
    north_col = []
    west_col = []
    inner_col = []
    east_col = []
    south_col = []



    for i in d:
        rules = {"anticedent":anticedent,"consequence":consequent,"confidence":confidence,"support":support,"lift":lift,"count":d[i],"subrub":i}
        if i in inner:
            
            sub = {i:rules}
            inner_col.append(sub)
            id_ = hashlib.sha256(json.dumps(rules, sort_keys=True).encode("utf-8")).hexdigest()
            rules["id"]=id_
            if innerCollection.find({"rules":{"$exists":True}}).count() ==0:
                innerCollection.update({"suburb":i}, {"$set":{"rules":[rules]}})
            else:
                if innerCollection.find({"rules.id":id_}).count() ==0:
                    innerCollection.find_one_and_update({"suburb": i},{"$push":{"rules":rules}})
        elif i in east:
            
            sub = {i:rules}
            east_col.append(sub)
            id_ = hashlib.sha256(json.dumps(rules, sort_keys=True).encode("utf-8")).hexdigest()
            rules["id"]=id_
            if easternCollection.find({"rules":{"$exists":True}}).count() ==0:
                easternCollection.update({"suburb":i}, {"$set":{"rules":[rules]}})
            else:
                if easternCollection.find({"rules.id":id_}).count() ==0:
                    easternCollection.find_one_and_update({"suburb": i},{"$push":{"rules":rules}})
        elif i in west:
            
            sub = {i:rules}
            west_col.append(sub)
            id_ = hashlib.sha256(json.dumps(rules, sort_keys=True).encode("utf-8")).hexdigest()
            rules["id"]=id_
            if westernCollection.find({"rules":{"$exists":True}}).count() ==0:
                westernCollection.update({"suburb":i}, {"$set":{"rules":[rules]}})
            else:
                if westernCollection.find({"rules.id":id_}).count() ==0:
                    westernCollection.find_one_and_update({"suburb": i},{"$push":{"rules":rules}})
        elif i in south:
            
            sub = {i:rules}
            south_col.append(sub)
            id_ = hashlib.sha256(json.dumps(rules, sort_keys=True).encode("utf-8")).hexdigest()
            rules["id"]=id_
            if southernCollection.find({"rules":{"$exists":True}}).count() ==0:
                southernCollection.update({"suburb":i}, {"$set":{"rules":[rules]}})
            else:
                if southernCollection.find({"rules.id":id_}).count() ==0:
                    southernCollection.find_one_and_update({"suburb": i},{"$push":{"rules":rules}})
        elif i in north:
            
            sub = {i:rules}
            north_col.append(sub)
            id_ = hashlib.sha256(json.dumps(rules, sort_keys=True).encode("utf-8")).hexdigest()
            rules["id"]=id_
            if northernCollection.find({"rules":{"$exists":True}}).count() ==0:
                northernCollection.update({"suburb":i}, {"$set":{"rules":[rules]}})
            else:
                if northernCollection.find({"rules.id":id_}).count() ==0:
                    northernCollection.find_one_and_update({"suburb": i},{"$push":{"rules":rules}})

    

    print("north")
    print (north_col)
    print("west")
    print(west_col)
    print("inner")
    print(inner_col)
    print("east")
    print(east_col)
    print("south")
    print(south_col)
   


# main({"QpsOffence":"UNLAWFUL_ENTRY"},{"Solved":False},0.12342891 , 0.8043754, 1.618343)
# main({"QpsOffence":"UNLAWFUL_ENTRY","Unemployment_rating":"LOW"},{"Solved":False},0.03961896 , 0.8155412 ,1.640807)
# main({"QpsOffence":"UNLAWFUL_ENTRY","Unemployment_rating":"MEDIUM"},{"Solved":False},0.04180984 , 0.8033177 ,1.616215)
# main({"QpsOffence":"UNLAWFUL_ENTRY","Unemployment_rating":"VERY LOW"},{"Solved":False},0.03440696 , 0.8023596, 1.614287) 
# main({"QpsOffence":"THEFT","Suburb":"FORTITUDE VALLEY"},{"Solved":False},0.01288153 , 0.7840161 ,1.577381) #prep
# main({"Solved":False,"Suburb":"BRISBANE CITY"},{"QpsOffence":"THEFT"},0.01964156,  0.6399455 ,1.896873)
# main({"Solved":False,"Suburb":"FORTITUDE VALLEY"},{"QpsOffence":"THEFT"},0.01288153 , 0.6369014 ,1.887850)
# main({"Solved":True,"Unemployment_rating":"LOW","Suburb":"KANGAROO POINT"},{"QpsOffence":"GOOD_ORDER"},0.00114877252862562,0.519895629484671,4.7573830674298)
# main({"Unemployment_rating":"LOW"},{"Solved":False},0.15077459 , 0.5120091 ,1.030124) 
# main({"Unemployment_rating":"MEDIUM"},{"Solved":True},0.19464415 , 0.5148754 ,1.023683) 
# main({"Unemployment_rating":"VERY LOW"},{"Solved":False},0.12392906 , 0.5094024 ,1.024879) 
main({"QpsOffence":"THEFT"},{"Solved":False}, 0.22375984 , 0.6632502 ,1.334409) #prep...
