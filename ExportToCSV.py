import numpy as np 
import pandas as pd 
from pymongo import MongoClient
from Offences import Offences

def objectToCSV():  
    client = MongoClient('localhost',27017)
    db = client.DataMining
    collection = db.Brisbane_South_new

    resultSet = []

    dataset = collection.find({})

    for i in dataset:
        
        for ii in i["OffenceInfo"]:
            temp = []
            temp.append(i["MeshBlockId"]) #0
            temp.append(ii["QpsOffenceId"]) #1
            temp.append(ii["Suburb"]) #2
            temp.append(ii["Postcode"]) #3
            temp.append(ii["OffenceCount"]) #4
            temp.append(Offences(ii["QpsOffenceCode"]).name) #5
            temp.append(ii["Solved"]) #6
            temp.append(ii["ReportDate"]) #7
            temp.append(ii["StartDate"]) #8
            temp.append(ii["EndDate"]) #9

            resultSet.append(temp)

    resultSet = np.array(resultSet)

    dataframe = pd.DataFrame(np.column_stack([resultSet[:,0], resultSet[:,1], 
    resultSet[:,2], resultSet[:,3], resultSet[:,4], resultSet[:,5], resultSet[:,6], resultSet[:,7], resultSet[:,8], resultSet[:,9]]),
    columns = ["MeshBlockId",'QpsOffenceId','Suburb','Postcode','OffenceCount','QpsOffence','Solved','ReportDate','StartDate','EndDate'])

    dataframe.to_csv("Brisbane_South.csv", sep=',', encoding= "utf-8")

objectToCSV()
    



