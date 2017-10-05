import numpy as np 
import pandas as pd 
from sklearn.cluster import DBSCAN, KMeans
from Offences import Offences
import time
from datetime import datetime
dataframe = pd.read_csv("./datasets_csv/Brisbane_South.csv",usecols=[0,1,2,3,4,5,6,7,8,9])

arr = dataframe.as_matrix()


offends_code = []
for i in arr[:,6]:
    
    if i == "GOOD_ORDER":
        offends_code.append(54)
    elif i=="DRUG":
        offends_code.append(45)
    elif i=="THEFT":
        offends_code.append(30)
    elif i=="PROPERTY_DAMAGE":
        offends_code.append(28)
    elif i=="HANDLING_STOLEN_GOODS":
        offends_code.append(39)
    elif i=="ASSAULT":
        offends_code.append(8)
    elif i=="UNLAWFUL_ENTRY":
        offends_code.append(21)
    elif i=="UNLAWFUL_MOTOR_VEHICLE":
        offends_code.append(29)
    elif i=="HOMOCIDE":
        offends_code.append(1)
    elif i=="ROBBERY":
        offends_code.append(14)
    elif i=="LIQUOR":
        offends_code.append(47)
    elif i=="FRAUD":
        offends_code.append(35)
    elif i=="ARSON":
        offends_code.append(27)

arr[:,6] = np.array(offends_code)
print (arr[:,6])


X= np.column_stack([arr[:,1],arr[:,5], arr[:,6],arr[:,7],[time.mktime(datetime.strptime(i,'%Y-%m-%dT%H:%M:%S').timetuple())/(1e9) for i in arr[:,8]]])

db = DBSCAN(eps=0.5, min_samples=5, metric='cosine', algorithm='brute',n_jobs=-1).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=None)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_
print (labels)


# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)


print('Estimated number of clusters: %d' % n_clusters_)
