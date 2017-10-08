import pandas as pd
import numpy as np
from datetime import date, datetime


def mergeSet():
    dataframe = pd.read_csv("../../../RData/CPI-Data-Brisbane-labeled.csv", usecols=[1, 3])
    dataframe1 = pd.read_csv("../../../Rdata/Brisbane_South.csv", usecols=[0, 4, 7])
    matrix_bne = dataframe1.as_matrix()
    cpi = dataframe.as_matrix()
    label = []

    temp = {}

    for i in cpi:
        temp[int(i[0])] = str(i[1])

    print(matrix_bne[:, 0])
    index = 0
    for i in matrix_bne[:, 0]:
        year = i
        if i == 2006:
            year = 2007
        label.append(temp[year])

    label = np.array(label)

    merged = np.column_stack([matrix_bne[:, 0], matrix_bne[:, 1],
                              matrix_bne[:, 2], label[:]])

    print(merged)

    X = []
    for i in merged:
        if i[-1] == None:
            continue
        X.append(i)

    X = np.array(X)

    df = pd.DataFrame(X,
                      columns=["Year", 'Suburb', 'OffenceType', 'CPI-Annual-Change'])

    df.to_csv("Brisbane_South_Merged_Information_CPI.csv", sep=',', encoding="utf-8")


mergeSet()