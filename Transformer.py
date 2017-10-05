from PoliceData import getGeoInfo
import json
import re


def idSuburb():

    with open('suburbs2.json') as f:
        suburbs = json.load(f)
    # pattern = re.compile("mt")

    root = {}


    for i in suburbs:
        temp = {}
        for ii in suburbs[i]:
            print (ii)
            suburb = ii.lower()
           
            # if pattern.match(suburb) != None:
            suburb = suburb.replace("mt","mount")
            
            profile = getGeoInfo(suburb)
            # print(profile)
            for j in profile["Result"]:
                
                if "LGA" in j:
                    print (j)
                    print (j["LGA"])
                    print (j["Name"])
                    if j["LGA"] == "BRISBANE CITY" and j["Name"]== suburb.upper():
                        print (j["QldSuburbId"])
                        temp[j["QldSuburbId"]] = suburb
                
        root[i] = temp

    with open('suburbID.json', 'w') as outfile:
        json.dump(root, outfile)           

idSuburb()

