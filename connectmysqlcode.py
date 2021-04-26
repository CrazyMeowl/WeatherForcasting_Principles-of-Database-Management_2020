import mysql.connector
import json
import time
import urllib.request

db = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	passwd = 'hehe',
	database = 'wherethefourcasting'
	)
mycursor = db.cursor()


#mycursor.execute('CREATE DATABASE wherethefourcasting') # query to create the data base
#mycursor.execute( 'CREATE TABLE Location (locationID int PRIMARY KEY NOT NULL, name VARCHAR(50), timezone int , region VARCHAR(50), country VARCHAR(50), longitude float, latitude float, elevation float)')
#mycursor.execute('CREATE TABLE Wfd ( wfddate DATE, mintemp int , maxtemp int, dayweather VARCHAR(30), nightweather VARCHAR(30), locationID int, FOREIGN KEY (locationID) REFERENCES location(locationID) )')


'''
mycursor.execute('DESCRIBE Person')

for x in mycursor:
	print(x)
'''

#mycursor.execute('INSERT INTO Person(name,age) VALUES (%s,%s)',('cara',19))
#db.commit()

'''
mycursor.execute('SELECT * FROM Person')

for x in mycursor:
	print(x)
'''

#DATE YYYY-MM-DD


#apikey = 'q651HeEBw5DCSyfxDwPoD64U4OSeGkpy'
apikey = 'tgF9JGfFQW0YKArJUP1cZECMeg6iQmMj'

def forecast():

	while True:
	
		searchURL = 'http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey='+apikey+'&q='+(input("Please enter the city name: ").replace(' ','%20'))
		with urllib.request.urlopen(searchURL) as searchJSON:
			datalocation = json.loads(searchJSON.read().decode())
	
		location_key = datalocation[0]['Key']
		#print(datalocation)
		#GET LOCATION detail DATA 
		locationdetailurl = 'http://dataservice.accuweather.com/locations/v1/'+str(location_key)+'?apikey='+apikey
		with urllib.request.urlopen(locationdetailurl) as detailJSON:
			locationdetail = json.loads(detailJSON.read().decode())
		#GET FORECAST DATA
		forecastURL = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/'+str(location_key)+'?apikey='+apikey+'&details=false&metric=true'
		#forecastURL = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/'+str(location_key)+'?apikey='+apikey+'&language=vi-vn&details=false&metric=true'
		#http://dataservice.accuweather.com/forecasts/v1/daily/5day/353981?apikey=q651HeEBw5DCSyfxDwPoD64U4OSeGkpy&language=vi-vn&details=false&metric=true
		with urllib.request.urlopen(forecastURL) as forecastJSON:
			dataforecast = json.loads(forecastJSON.read().decode())
		#print(dataforecast)
		return dataforecast,datalocation,locationdetail
		
		#1 hour hourly patern
		#http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/353981?apikey=q651HeEBw5DCSyfxDwPoD64U4OSeGkpy&metric=true
		#12 hour hourly
		#http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/353981?apikey=q651HeEBw5DCSyfxDwPoD64U4OSeGkpy&metric=true


def searchCity():
	while True:
	
		searchURL = 'http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey='+apikey+'&q='+(input("Please enter the city name: ").replace(' ','%20'))

		with urllib.request.urlopen(searchURL) as searchJSON:
			datalocation = json.loads(searchJSON.read().decode())
	
		location_key = datalocation[0]['Key']
		return location_key

def getCitydetail(location_key):



	locationdetailurl = 'http://dataservice.accuweather.com/locations/v1/'+str(location_key)+'?apikey='+apikey
	
	with urllib.request.urlopen(locationdetailurl) as detailJSON:
		locationdetail = json.loads(detailJSON.read().decode())

		ld = locationdetail
		_ID = ld['Key']
		_name = ld['EnglishName']
		_timezone = ld['TimeZone']['GmtOffset']
		_region = ld['Region']['EnglishName']
		_country = ld['Country']['EnglishName']
		_latitude = ld['GeoPosition']['Latitude']
		_longitude = ld['GeoPosition']['Longitude']
		_elevation = ld['GeoPosition']['Elevation']['Metric']['Value']
		#print((_ID,_name,_timezone,_region,_country,_longitude,_latitude,_elevation))
		return _ID,_name,_timezone,_region,_country,_longitude,_latitude,_elevation
		

while True:
	try:
		a = searchCity()
		_ID,_name,_timezone,_region,_country,_longitude,_latitude,_elevation = getCitydetail(a)
		print((_ID,_name,_timezone,_region,_country,_longitude,_latitude,_elevation))
		promt = input("Do you want to save the information to the database (Y/N)")
		if 'y' in promt or 'Y' in promt:
			mycursor.execute('INSERT INTO location(locationID,name,timezone,region,country,longitude,latitude,elevation) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(_ID,_name,_timezone,_region,_country,_longitude,_latitude,_elevation))
			db.commit()
	except:
		print("Try again")