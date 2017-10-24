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
        if (str(i[2]) + "_"+str(i[5])+"_"+ i[-1]) not in aggregate:
            # not recorded yet
            count = int(i[3]) 
            aggregate [str(i[2]) + "_" +str(i[5])+ "_" + i[-1]] = {str(i[4]): count}
        else:
            # recorded
            # print ([str(i[0]) + "_"+str(i[5])+"_"+ i[-1]] )
            crimeCounts = aggregate [str(i[2]) + "_"+str(i[5])+"_"+ i[-1]] 
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
    
    # temp = []
    # for i in aggregate:
    #     total = 0
    #     offences = []
    #     for ii in aggregate[i]:
    #         total += int(aggregate[i][ii])
    #         t1= (ii, aggregate[i][ii])
    #         offences.append(t1)
    #     strings = i.split("_")
    #     for ii in offences:
    #         temp.append([strings[0], strings[1],strings[2],ii[0], ii[1]])
    # print (total)
    # print (temp)

    # temp = np.array(temp)
    # df = pd.DataFrame(np.column_stack([temp[:,0], temp[:,1],temp[:,2],temp[:,3],temp[:,4]]),
    # columns = ["MeshBlockId",'Solved','Unemployment_rating', 'QpsOffence', 'TotalOffences'])

    # df.to_csv("Summary_Offences.csv", sep=',', encoding= "utf-8")
    return aggregate

def getNumberOfCrimeInSuburb(suburb, solved="TRUE", rate="LOW"):
    sumz = summerizer()

    key = suburb+"_"+solved+"_"+rate
    crimesNum = sumz[key]
    total=0
    for i in crimesNum:
        
        
        total += crimesNum[i]
    return total


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
    areas_low = {}
    areas_high = {}
    areas_med = {}
    areas_vlow = {}
    areas_vhigh = {}

    for i in matrix2:
        for j in result:
            
            lrule1 = j[0][0][lhs[0]] #unemployment rating
            lrule2 = j[0][0][lhs[1]] #offence
            # print(lrule2)
            rrule = bool(j[0][1][rhs[0]]) #solved

            if i[-1] == lrule1 and i[4]==lrule2 and i[5] == rrule:

                """
                    for {Unemployment_rating=LOW, QpsOffence=UNLAWFUL_ENTRY} => {Solved=False} 
                """

                if i[-1]=="LOW" and i[4]=="UNLAWFUL_ENTRY" and bool(i[5])==False:

                    if i[2] not in areas_low:
                        areas_low[i[2]]= i[3]
                    else:
                        count = areas_low[i[2]]
                        count+=i[3]
                        areas_low[i[2]]=count
                
                # if lrule == "UNLAWFUL_ENTRY":
                #     if i[2] not in areas_high:
                #         areas_high[i[2]]= i[3]
                #     else:
                #         count = areas_high[i[2]]
                #         count+=i[3]
                #         areas_high[i[2]]=count
                        
                # elif lrule == "THEFT":
                #     if i[2] not in areas_vhigh:
                #         areas_vhigh[i[2]]= i[3]
                #     else:
                #         count = areas_vhigh[i[2]]
                #         count+=i[3]
                #         areas_vhigh[i[2]]=count
                # elif lrule == "VERY LOW":
                #     if i[2] not in areas_vlow:
                #         areas_vlow[i[2]]= i[3]
                #     else:
                #         count = areas_vlow[i[2]]
                #         count+=i[3]
                #         areas_vlow[i[2]]=count
                # elif lrule == "LOW":
                #     if i[2] not in areas_low:
                #         areas_low[i[2]]= i[3]
                #     else:
                #         count = areas_low[i[2]]
                #         count+=i[3]
                #         areas_low[i[2]]=count
                # elif lrule == "MEDIUM":
                #     if i[2] not in areas_med:
                #         areas_med[i[2]]= i[3]
                #     else:
                #         count = areas_med[i[2]]
                #         count+=i[3]
                #         areas_med[i[2]]=count

    print(areas_high)
    print(areas_low)
    print(areas_vhigh)
    print(areas_vlow)
    print(areas_med)


    # df = pd.DataFrame(np.column_stack([list(areas_high.keys()), [ areas_high[i] for i in list(areas_high.keys())]]),
    # columns = ["UNLAWFUL_ENTRY", "Count"])

    # df.to_csv("areas_entry_solved.csv", sep=',', encoding= "utf-8")

    # df = pd.DataFrame(np.column_stack([list(areas_vhigh.keys()), [ areas_vhigh[i] for i in list(areas_vhigh.keys())]]),
    # columns = ["THEFT", "Count"])

    # df.to_csv("areas_theft_solved.csv", sep=',', encoding= "utf-8")

    # df = pd.DataFrame(np.column_stack([list(areas_low.keys()), [ areas_low[i] for i in list(areas_low.keys())]]),
    # columns = ["Low", "Count"])

    # df.to_csv("areas_low_solved.csv", sep=',', encoding= "utf-8")
    
    # df = pd.DataFrame(np.column_stack([list(areas_vlow.keys()), [ areas_vlow[i] for i in list(areas_vlow.keys())]]),
    # columns = ["Very Low", "Count"])

    # df.to_csv("areas_vlow_solved.csv", sep=',', encoding= "utf-8")

    # df = pd.DataFrame(np.column_stack([list(areas_med.keys()), [ areas_med[i] for i in list(areas_med.keys())]]),
    # columns = ["Medium", "Count"])

    # df.to_csv("areas_med_solved.csv", sep=',', encoding= "utf-8")
                
def getDatas(unemployment="MEDIUM", crime ="UNLAWFUL_ENTRY", Solved =False, Suburb=None):

    dataframe1 = pd.read_csv("./datasets_csv/All_datas.csv",usecols=[1,2,3,5,6,7,8,10])
   
    matrix2 = dataframe1.as_matrix().tolist()
    areas = {}

    for i in matrix2:
        
        if  i[4]==crime and bool(i[5])==Solved :
        # if bool(i[5])==Solved and i[4]==crime and i[2] == unemployment: #unemployment == suburb
        # if  i[2] == unemployment and bool(i[5])==crime and i[4]==Solved: #crime = solved ,unemploment ==suburb, Solved == crime
            if i[2] not in areas:
                areas[i[2]]= i[3]
            else:
                count = areas[i[2]]
                count+=i[3]
                areas[i[2]]=count
    
    print(areas)
    return areas
                