from datetime import date, datetime, timedelta
import json
from LocationType import LocationType
from PoliceData import getOffences
from Offences import Offences
from pprint import pprint
from pymongo import MongoClient
import threading

def date_range(start, end, intv=3):
    
    # start = datetime.strptime(start,"%Y%m%d")
    # end = datetime.strptime(end,"%Y%m%d")
    diff = (end  - start ) / intv
    for i in range(intv):
        yield (start + diff * i)
    yield end

def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

def generateStartEndDate(period=9):
    temp =[]
    starter = "20120101"
    for i in range(period):
        if type(starter) == str:
            starter = datetime.strptime(starter,"%Y%m%d").date()
        final_year = add_years(starter,1)
        # print(final_year)
        dateRange = list(date_range(starter,final_year))
        for ii in range(len(dateRange)):
            if ii != len(dateRange)-1:
                # print(dateRange[ii])
                temp.append((dateRange[ii], dateRange[ii+1] ))

        starter = final_year
    return temp

def multiCaller(suburb, locations, offendTypes, dates):
  
    client = MongoClient('localhost',27017)
    db = client.DataMining
    collection = None
    if suburb.lower() == "brisbane_east":
        collection = db.Brisbane_East
    elif suburb.lower() == "brisbane_west":
        collection = db.Brisbane_West
    elif suburb.lower() == "brisbane_inner":
        collection = db.Brisbane_Inner
    elif suburb.lower() == "brisbane_north":
        collection = db.Brisbane_North
    elif suburb.lower() == "brisbane_south":
        collection = db.Brisbane_South_new  
    
    # for j in dates:
            # print (i[0],i[1])
    try:

        offences = getOffences(locations, date(2017,5,2), date(2017,9,1), offendTypes) # 31 december to 1 January 2008

        for i in offences["Result"]:
            try:
                report = collection.find({"MeshBlockId": i["MeshBlockId"]})
                if report.count() >0:
                    # the given statistical region exists in db so just edit them
                    print (i["MeshBlockId"])
                    for ii in i["OffenceInfo"]:
                        print (ii["QpsOffenceId"])
                        if collection.find({"OffenceInfo":{"$elemMatch":{"QpsOffenceId":ii["QpsOffenceId"]}}}).count() ==0:
                            # if a crime on one statistical region has not existed on db, append it to OffenceInfo
                            # OpsOffenceId is UNIQUE
                            print ("Pure new ",ii["QpsOffenceId"])
                            collection.find_one_and_update({"MeshBlockId": i["MeshBlockId"]},{"$push":{"OffenceInfo":ii}})
                            print ("new offences have been appended")
                else:

                    # new Mesh Statistical Region
                    print (i["MeshBlockId"])
                    collection.insert(i)
                    print ("new regional information has been stored")

            except Exception as e1:
            
                print (e1)
                    
    except Exception as e:
        print (e)
        return False

    # db.close()
    return True

def detailProvider(suburb, dates):

    print (suburb)
    #pull Brisbane Inner first

    with open("suburbID.json") as f:
        suburbs = json.load(f)

    locations = []

    for i in suburbs[suburb]:
        
        locations.append(i)
    
    offendTypes = [Offences.ARSON, Offences.ASSAULT, Offences.DRUG, Offences.FRAUD, Offences.GOOD_ORDER,
        Offences.HANDLING_STOLEN_GOODS, Offences.HOMOCIDE, Offences.LIQUOR, Offences.PROPERTY_DAMAGE, Offences.ROBBERY,
        Offences.THEFT, Offences.UNLAWFUL_ENTRY, Offences.UNLAWFUL_MOTOR_VEHICLE]


    status = multiCaller(suburb, locations, offendTypes, dates)
    
    print (status)
    # return status


def main():
    # suburbs = ["Brisbane_inner","Brisbane_south", "Brisbane_north", "Brisbane_west","Brisbane_east"]
    suburbs = ["Brisbane_west"]
    # Multi Thread Job for inner and east for 5 years period from 1 January 2012
    # Single Thread Job for north for 3 years (Now 1) period from 1 January 2016
    g = generateStartEndDate(period=5)
    threads = [threading.Thread(target=detailProvider, args=(suburb,g,)) for suburb in suburbs]
    for thread in threads:
        print (thread)
        thread.start()
    for thread in threads:
        thread.join()

main()

