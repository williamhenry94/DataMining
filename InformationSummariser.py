from datetime import date, datetime
import pandas as pd  
import numpy as np 

def summerizer():
    
    dataframe = pd.read_csv("./datasets_csv/All_datas.csv",usecols=[1,2,3,5,6,7,8,10])

    matrix = dataframe.as_matrix()
    matrix = matrix.tolist()

    aggregate = {}
    
    for i in matrix:
        # print(i)
        count = 0
        if (str(i[0]) + "_"+str(i[5])+"_"+ i[-1]) not in aggregate:
            # not recorded yet
            count = int(i[3]) 
            aggregate [str(i[0]) + "_" +str(i[5])+ "_" + i[-1]] = {str(i[4]): count}
        else:
            # recorded
            # print ([str(i[0]) + "_"+str(i[5])+"_"+ i[-1]] )
            crimeCounts = aggregate [str(i[0]) + "_"+str(i[5])+"_"+ i[-1]] 
            # print (crimeCounts)
            if str(i[4]) in crimeCounts:
                count = crimeCounts[str(i[4])]
                count += int(i[3])
                crimeCounts[str(i[4])] = count
            else:
                crimeCounts[str(i[4])] = int(i[3])


            
            # print([str(i[0]) + str(i[5])])
            
            # for ii in temp:
            #     # print(temp)
            #     if ii[0][0] ==str(i[4]):

                
            #         # the type of the crime has been recorded
            #         # print(i[4])
                   
            #         # print(i[-1])
            #         # print(ii[-1])
            #         #if the type of crime has been recorded and same unemployment rate just increment it.
            #         count = ii[0][1]
            #         count += int(i[3])
            #         ii[0][1] = count


                    
                
            #             # print ("added")
            #             # print(temp)
                    
                   
                       
            #     else:
                
            #         count = int(i[3]) 
            #         X = temp[:]
            #         X.append([[str(i[4]),count], i[-1]])
            #         temp = X

            # aggregate [str(i[0]) + "_"+str(i[5])+"_"+ i[-1]]   = temp
                

    # print (aggregate)
    
    temp = []
    for i in aggregate:
        total = 0
        offences = []
        for ii in aggregate[i]:
            total += int(aggregate[i][ii])
            t1= (ii, aggregate[i][ii])
            offences.append(t1)
        strings = i.split("_")
        for ii in offences:
            temp.append([strings[0], strings[1],strings[2],ii[0], ii[1]])
    # print (total)
    # print (temp)

    temp = np.array(temp)
    df = pd.DataFrame(np.column_stack([temp[:,0], temp[:,1],temp[:,2],temp[:,3],temp[:,4]]),
    columns = ["MeshBlockId",'Solved','Unemployment_rating', 'QpsOffence', 'TotalOffences'])

    df.to_csv("Summary_Offences.csv", sep=',', encoding= "utf-8")


def extractRules(lhs,rhs,strict=False):
    dataframe = pd.read_csv("./rules/association_rules.csv",usecols=[0,1,2,3])
    dataframe1 = pd.read_csv("./datasets_csv/All_datas.csv",usecols=[1,2,3,5,6,7,8,10])
    matrix = dataframe.as_matrix()
    matrix2 = dataframe1.as_matrix().tolist()

    rules = []
    for i in matrix[:,0]:
        splits = i.split(" => ")
        norm1= [ ii.replace("{","").replace("}","") for ii in splits]
        lrhs = []
        for ii in norm1:
            temp ={}
            # check for composite rules in one hand side
            composite = ii.split(",")
            if len(composite) >1:
                for iii in composite:
                    
                    k,v = iii.split("=")
                    temp[k] = v
            else:
                k,v = ii.split("=")
                temp[k]=v
            lrhs.append(temp)
        rules.append(lrhs)
    
    
    
    

    # print(rules)

    if type(lhs) and type(rhs) != list:
        return Exception("ValueError")
    result = []
    for i in range(len(rules)):
        lhsRules = rules[i][0] #lhs
        lKeys = set(list(lhsRules.keys()))
        l = set(lhs)
        rhsRules = rules[i][1] #rhs
        rKeys = set(list(rhsRules.keys()))
        r = set(rhs)
        if strict == True:
           
            if len(lKeys-l) == 0 and len(rKeys-r)==0:
                result.append((rules[i],i))
        else:
           
            if len(l-lKeys) == 0 and len(r-rKeys)==0:
                result.append((rules[i],i))
    

    print(result)
    areas_low = set()
    areas_high = set()
    areas_med = set()
    areas_vlow = set()
    areas_vhigh = set()
    for i in matrix2:
        for j in result:
            lrule = j[0][0][lhs[0]]
            rrule = j[0][1][rhs[0]]
            if i[-1] == lrule  and i[4] == rrule:
                if lrule == "HIGH":
                    areas_high.add(i[2])
                elif lrule == "VERY HIGH":
                    areas_vhigh.add(i[2])
                elif lrule == "VERY LOW":
                    areas_vlow.add(i[2])
                elif lrule == "LOW":
                    areas_low.add(i[2])
                elif lrule == "MEDIUM":
                    areas_med.add(i[2])

    print(areas_high)
    print(areas_low)
    print(areas_vhigh)
    print(areas_vlow)
    print(areas_med)
                
   








    
extractRules(["Unemployment_rating"],["QpsOffence"],strict=False)
                