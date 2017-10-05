from PoliceData import getGeoInfo, getOffences
from LocationType import LocationType
from pprint import pprint


data = getGeoInfo("moreton island", maxResult=10)
pprint (data)
# offences = getOffences(location="asd", startDate=123, endDate=123, offences=8)
# pprint (offences)p