#This is the weather forecast ap developed for the Python challenge

import time
start = time.time()

import urllib2
import xml.etree.ElementTree as ET
from pyzipcode import ZipCodeDatabase
from urllib import quote

def check_units(units):
    while True:
        if units == 'imperial' or units == 'metric' or units == 'f' or units == 'c':
            return units
            break
        else:
            print "That is not a valid entry"
            units = raw_input("What units would you like the temperature in? You may choose 'imperial' or 'metric': ")
 
location = raw_input("For what city would you like a weather forecast? (You may also enter a valid United States zip code): ")      

def getWeather(location):
    if location.isdigit():
        zipData = ZipCodeDatabase()
        zipCode = zipData[int(location)]
        location = zipCode.city
        units = lower(raw_input("What units would you like the temperatur in? ('c' or 'metric' for example): "))
	if units == 'f':
		units = 'imperial'
	elif units == 'c':
		units = 'metric'
        check_units(units)        
        country = "us"
    else:
        location = quote(location)
        units = raw_input("What units would you like the temperature in? You may choose 'imperial' or 'metric': ")
        check_units(units)
        country = raw_input("Please enter the name of country this city is located in. You may also enter its common two letter abbreviation. (Ex: Fr = France, JP = Japan, US = United States: ")
    cnt = raw_input("How many days would you like the forecast for? Please enter a number between 1 and 14: ")
    while cnt > 14 and cnt < 1:
        print "That is not a valid entry"
        cnt = raw_input("Please enter a number between 1 and 14: ") 
    searchParam = "http://api.openweathermap.org/data/2.5/forecast/daily?q=" + location + "," + country + '&mode=xml&units='+ units +'&cnt=' + cnt
    weatherData = urllib2.urlopen(searchParam)
    rawData = str(weatherData.read())
    root = ET.fromstring(rawData)
    forecastHi = []
    forecastLo = []
    date = []
    if units == 'imperial':
        degreeUnit = 'F'
    else:
        degreeUnit = 'C'
    for time in root.iter('time'):
        date.append(time.attrib['day'])
    for temperature in root.iter('temperature'):
        forecastHi.append(temperature.attrib['max'])
    for temperature in root.iter('temperature'):
        forecastLo.append(temperature.attrib['min'])  
    return location, degreeUnit, forecastHi, forecastLo, date 

(city, degree, highs, lows, dates) = getWeather(location)

for i in dates:
    print"The high temp for ", city,  "on ",  i,  " is ", highs[dates.index(i)], degree
    print"The low temp for ", city,  "on ",  i,  " is ", lows[dates.index(i)], degree
    
end = time.time()
print end - start
