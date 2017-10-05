import urllib3
from urllib3.util import parse_url
import matplotlib.pyplot as plt
from matplotlib import style
from shapely.wkt import loads
import json
from selenium import webdriver
import time
import redis
from datetime import date

from LocationType import LocationType

def getRedisClient():

    r = redis.StrictRedis(host='localhost',port=6379)
    return r

def getChromeDriver():

    driver = webdriver.Chrome("/Users/williamhenry/Downloads/chromedriver-2")
    return driver

def getGeoInfo(location, maxResult=5):

    location = location.replace(" ","%20")
    http = urllib3.PoolManager()
    url = "https://data.police.qld.gov.au/api/boundary?name="+location+"&returngeometry=true&maxresults="+ str(maxResult)
    
    req = http.request('GET', url )

    if (req.status ==200):
        data = json.loads(req.data.decode("UTF-8"))
        return data
    else:
        return Exception ("HTTP Request Failed")

def getOffences( location, startDate, endDate, offences, locType=LocationType.SUBURB):

    http = urllib3.PoolManager()

    offencesString = ""

    for i in range(len(offences)):
        if i != (len(offences)-1):
            offencesString += str((offences[i]).value) +","
        else:
            offencesString += str((offences[i]).value)

    # offencesString = ",".join(offences)

    if type(startDate) != date or type(endDate) != date:
        raise TypeError("startDate and endDate must be date!")

    startDate = str(int(time.mktime(startDate.timetuple())))

    endDate = str(int(time.mktime(endDate.timetuple())))

    if type(location) != list:
        raise TypeError("Location must be a list type!")
    
    locationString = ""
    for i in range(len(location)):
        if i != (len(location)-1):
            locationString+=str(locType.value) + "_"+ str(location[i])+","
        else:
            locationString+=str(locType.value) + "_"+ str(location[i])

    url = "https://data.police.qld.gov.au/api/qpsmeshblock?boundarylist="+locationString+"&startdate="+startDate+"&enddate="+endDate+"&offences="+offencesString
    print(url)
    req = http.request('GET', url)
    
    if (req.status ==200):
        print ("OK")
        data = json.loads(req.data.decode("UTF-8"))
        return data
    else:
        return Exception ("HTTP Request Failed")

def getListOfSuburbs():
    driver = getChromeDriver()
    driver.get("https://www.brisbane.qld.gov.au/about-council/council-information-rates/brisbane-suburbs#v")
    time.sleep(5)
    # print (driver.title)
    
    texts = driver.find_elements_by_xpath("//td//strong")
    suburbs = []
    for i in texts:
        suburbs.append(i.text)
    return suburbs

def getRegionalPart():
    driver = getChromeDriver()
    r = getRedisClient()
    suburbs = json.loads(r.get("suburb"))
    print(len (suburbs))
    driver.get("https://en.wikipedia.org/w/index.php?title=List_of_Brisbane_suburbs&action=edit&section=6")
    time.sleep(5)

    # temp ={}
    # temp["Brisbane_inner"] = []
    # temp["Brisbane_north"] = []
    # temp["Brisbane_south"] = []
    # temp["Brisbane_east"] = []
    # temp["Brisbane_west"] = []

    with open('suburbs2.json') as f:
        temp = json.load(f)
    
    for i in suburbs:
        if driver.find_elements_by_xpath("//textarea[contains(text(),'"+i+"')]"):
            if i not in temp["Brisbane_west"]:
                (temp["Brisbane_west"]).append(i)
                print ((i,"Brisbane_west"))
           

    print (temp)
    with open('suburbs2.json', 'w') as outfile:
        json.dump(temp, outfile)

# getRegionalPart()
# s = getListOfSuburbs()
# r.set("suburb", json.dumps(s))
# print (s)
# print (len(s))




