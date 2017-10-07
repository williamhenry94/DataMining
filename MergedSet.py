import pandas as pd 
import numpy as np 
from datetime import date, datetime


def mergeSet():

    dataframe = pd.read_csv("./datasets_csv/Employment-Data-Brisbane-labeled.csv",usecols=[1,3])
    dataframe1 = pd.read_csv("./datasets_csv/Brisbane_inner.csv",usecols=[1,2,3,4,5,6,7,8,9])
    matrix_bne = dataframe1.as_matrix()
    emp = dataframe.as_matrix()
    label = []

    temp = {}

    for i in emp:
        temp[int(i[0])] = str(i[1])
    

    print(matrix_bne[:,7])
    index = 0
    for i in matrix_bne[:,7]:
        
        dt = datetime.strptime(i, '%Y-%m-%dT%H:%M:%S')
        year = int(dt.year)
        if year == 2006:
            label.append(temp[2007])
        else:
            if dt.month >6:
                if year !=2017:
                    label.append(temp[year+1])
                else:
                    label.append(None)
            else:
                label.append(temp[year])

    label = np.array(label)

    merged = np.column_stack([matrix_bne[:,0], matrix_bne[:,1], 
        matrix_bne[:,2], matrix_bne[:,3], matrix_bne[:,4], matrix_bne[:,5], matrix_bne[:,6], matrix_bne[:,7], matrix_bne[:,8], label[:]])

    

    X = []
    for i in merged:
        if i[-1] == None:
            continue
        X.append(i)

    X= np.array(X)


    df = pd.DataFrame(X,
        columns = ["MeshBlockId",'QpsOffenceId','Suburb','Postcode','OffenceCount','QpsOffence','Solved','ReportDate','StartDate','Label'])

    df.to_csv("Brisbane_Inner_Merged_Information.csv", sep=',', encoding= "utf-8")

mergeSet()