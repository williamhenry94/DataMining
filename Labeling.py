import numpy as np 
import pandas as pd 
from sklearn.cluster import DBSCAN, KMeans
from Offences import Offences
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn import metrics

def getProgressiveClassOfUnemployment():
    dataframe = pd.read_csv("./datasets_csv/Employment-Data-Brisbane.csv",usecols=[0,6])

    arr = dataframe.as_matrix()

    X = []


    for i in arr:
        if i[0] >=2000:
            i[0] = i[0]-2000
            X.append(i)

    X = np.array(X)
    print(X)
    db = DBSCAN(eps=1.2, min_samples=2, metric='euclidean', algorithm='brute').fit(X) # good with eps=1.2 and min_samples=3

    core_samples_mask = np.zeros_like(db.labels_, dtype=None)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_


    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)


    print('Estimated number of clusters: %d' % n_clusters_)

    print("Silhouette Coefficient: %0.3f"
            % metrics.silhouette_score(X, labels))


    for i in X:
        i[0] += 2007

    string_label =[]
    for i in range(len(labels)):
        if labels[i] == 0:
            string_label.append("LOW")
        if labels[i] == 1:
            string_label.append("MEDIUM")
        if labels[i] == 2:
            string_label.append("HIGH")
        if labels[i] == -1:
            string_label.append("VERY_HIGH")

    string_label = np.array(string_label)
    df = pd.DataFrame(np.column_stack([X[:,0], X[:,1],string_label[:]]),
    columns = ["MeshBlockId",'Unemployment Rate (%)','label'])

    df.to_csv("Employment-Data-Brisbane-labeled.csv", sep=',', encoding= "utf-8")

def getProgressiveClassOfCPI():
    dataframe = pd.read_csv("./datasets_csv/Consumer_Price_Index_of_Brisbane_March_Quarter_1999_to_June_Quarter_2017.csv",usecols=[0,1,3,4])

    arr = dataframe.as_matrix()

    X = []


    for i in arr:
        if i[0] >=2006 and i[0]!=2017:
            if i[1]==12:
                i[0] = i[0]-2006
                X.append([i[0],i[-1]])
        elif i[0]==2017:
            if i[1]==6:
                i[0] = i[0]-2006
                X.append([i[0],2.3])

    X = np.array(X)
    print(X)
    # db = DBSCAN(eps=1.192, min_samples=2, metric='euclidean', algorithm='brute').fit(X) # good with eps=1.2 and min_samples=3

    # core_samples_mask = np.zeros_like(db.labels_, dtype=None)
    # core_samples_mask[db.core_sample_indices_] = True
    

    kmeans = KMeans(n_clusters=12).fit(X)

    labels = kmeans.labels_
    kc = kmeans.cluster_centers_
    print (labels)
    print (kmeans.score(X))
    plt.scatter(X[:,0],X[:,1],hold=True, marker="o")
    plt.scatter(kc[:,0],kc[:,1],marker="*")
    plt.show()


    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)


    print('Estimated number of clusters: %d' % n_clusters_)

    print("Silhouette Coefficient: %0.3f"
            % metrics.silhouette_score(X, labels))


    # for i in X:
    #     i[0] += 2007

    # string_label =[]
    # for i in range(len(labels)):
    #     if labels[i] == 0:
    #         string_label.append("LOW")
    #     if labels[i] == 1:
    #         string_label.append("MEDIUM")
    #     if labels[i] == 2:
    #         string_label.append("HIGH")
    #     if labels[i] == -1:
    #         string_label.append("VERY_HIGH")

    # string_label = np.array(string_label)
    # df = pd.DataFrame(np.column_stack([X[:,0], X[:,1],string_label[:]]),
    # columns = ["MeshBlockId",'Unemployment Rate (%)','label'])

    # df.to_csv("Employment-Data-Brisbane-labeled.csv", sep=',', encoding= "utf-8")  


def getInterval():
    
    dataframe = pd.read_csv("./datasets_csv/Employment-Data-Brisbane.csv",usecols=[0,6])

    arr = dataframe.as_matrix()

    X = []


    for i in arr:
        if i[0] >=2000:
            i[0] = i[0]-2000
            X.append(i)

    X = np.array(X)
    

    temp = []
    hist = plt.hist(X[:,1],bins=5)
    
    
    interval = hist[1]
    
    for i in range(len(interval)):
        if i != len(interval)-1:
            temp.append((interval[i], interval[i+1]))

    for i in X:
        i[0] += 2000

    string_label =[]
    for i in X:

        if temp[0][0]<= i[1] and i[1]<=temp[0][1]:
            
            string_label.append("VERY LOW")
       
        elif temp[1][0]<= i[1] and i[1]<=temp[1][1]:
            
            string_label.append("LOW")
        elif temp[2][0]<= i[1] and i[1]<=temp[2][1]:
            
            string_label.append("MEDIUM")
        elif temp[3][0]<= i[1] and i[1]<=temp[3][1]:
            
            string_label.append("HIGH")
        elif temp[4][0]<= i[1] and i[1]<=temp[4][1]:
            
            string_label.append("VERY HIGH")

    string_label = np.array(string_label)
    
    df = pd.DataFrame(np.column_stack([X[:,0], X[:,1],string_label[:]]),
    columns = ["MeshBlockId",'Unemployment Rate (%)','label'])

    df.to_csv("Employment-Data-Brisbane-labeled.csv", sep=',', encoding= "utf-8")


def getIntervalSummary():
    
    dataframe = pd.read_csv("./datasets_csv/Summary_Offences.csv",usecols=[1,2,3,4,5])

    arr = dataframe.as_matrix()

    

    temp = []
    print((arr[:,4]).tolist())
    hist = plt.hist(arr[:,4],bins=10)
    # plt.show()
    
    print (hist)
    interval = hist[1]
    
    for i in range(len(interval)):
        if i != len(interval)-1:
            temp.append((interval[i], interval[i+1]))

    string_label =[]
    for i in arr[:,4]:
        
        
        if temp[0][0]<= i and i<=temp[0][1]:
            
            string_label.append("CAT1")
       
        elif temp[1][0]<= i and i<=temp[1][1]:
            
            string_label.append("CAT2")
        elif temp[2][0]<= i and i<=temp[2][1]:
            
            string_label.append("CAT3")
        elif temp[3][0]<= i and i<=temp[3][1]:
            
            string_label.append("CAT4")
        elif temp[4][0]<= i and i<=temp[4][1]:
            
            string_label.append("CAT5")
        elif temp[5][0]<= i and i<=temp[5][1]:
            
            string_label.append("CAT6")
        elif temp[6][0]<= i and i<=temp[6][1]:
            
            string_label.append("CAT7")
        elif temp[7][0]<= i and i<=temp[7][1]:
            
            string_label.append("CAT8")
        elif temp[8][0]<= i and i<=temp[8][1]:
            
            string_label.append("CAT9")
        elif temp[8][0]<= i and i<=temp[9][1]:
            
            string_label.append("CAT10")
        
       
        

    string_label = np.array(string_label)
    # print(len(string_label))
    # print(len(arr[:,0]))
    df = pd.DataFrame(np.column_stack([arr[:,0], arr[:,1],arr[:,2],arr[:,3],arr[:,4],string_label[:]]),
    columns = ["MeshBlockId",'Solved','Unemployment_rating','QpsOffence','TotalOffences','TotalOffencesLabel'])

    df.to_csv("Summary_Offences_Labeled.csv", sep=',', encoding= "utf-8")
    
def getCPIInterval():
    dataframe = pd.read_csv("../../../RData/CPI_Financial_Year_Change_Brisbane.csv", usecols=[0, 2])

    arr = dataframe.as_matrix()

    X = []

    for i in arr:
        i[0] = i[0] - 2000
        X.append(i)

    X = np.array(X)

    temp = []
    hist = plt.hist(X[:, 1], bins=5)

    interval = hist[1]

    for i in range(len(interval)):
        if i != len(interval) - 1:
            temp.append((interval[i], interval[i + 1]))

    for i in X:
        i[0] += 2000



    string_label = []
    for i in X:

        if temp[0][0] <= i[1] and i[1] <= temp[0][1]:

            string_label.append("VERY LOW")

        elif temp[1][0] <= i[1] and i[1] <= temp[1][1]:

            string_label.append("LOW")
        elif temp[2][0] <= i[1] and i[1] <= temp[2][1]:

            string_label.append("MEDIUM")
        elif temp[3][0] <= i[1] and i[1] <= temp[3][1]:

            string_label.append("HIGH")
        elif temp[4][0] <= i[1] and i[1] <= temp[4][1]:

            string_label.append("VERY HIGH")


    string_label = np.array(string_label)
    print(string_label)

    df = pd.DataFrame(np.column_stack([X[:, 0], X[:, 1], string_label[:]]),
                      columns=["Year", 'Annual Change (%)', 'label'])

    df.to_csv("CPI-Data-Brisbane-labeled.csv", sep=',', encoding="utf-8")
    


getCPIInterval()
getIntervalSummary()

