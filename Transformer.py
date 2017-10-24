from PoliceData import getGeoInfo
import json
import re
import pandas as pd


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


def getMeshSubrubRelation():
    dataframe = pd.read_csv("./datasets_csv/All_datas.csv",usecols=[1,3])

    arr = dataframe.as_matrix()
    meshSuburbs = {}
    for i in arr:
        if i[1] not in meshSuburbs:
            a = set()
            a.add(i[0])
            meshSuburbs[i[1]] = a
        else:
            temp = meshSuburbs[i[1]]
            temp.add(i[0])
            meshSuburbs[i[1]] = temp
    
    for i in meshSuburbs:
        meshSuburbs[i] = list(meshSuburbs[i])
    print(meshSuburbs)

    with open('meshSuburbs.json', 'w') as outfile:
        json.dump(meshSuburbs, outfile)      


getMeshSubrubRelation()

