


import urllib.request as req
import time
import json
from json import JSONDecoder
import datetime
import sqlite3

def parseJson(conn, jsonStr, company,tag):

    try:
        bikes = json.loads(jsonStr)['bike']
        date = str(datetime.date.today())
        #conn = sqlite3.connect('ShareBikes.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Bikes
                 (id text, lng real, lat real, bikeType integer, date text, company text, ''' \
                  + '''region text, tag text, PRIMARY KEY (id, company, tag))''')
        for bike in bikes :
            id = bike['distId']
            lat = bike['distY']
            lng = bike['distX']
            region = getRegion(lat, lng)
            bikeType = bike['biketype']
            try :               
                storeToDb(c, id, lng, lat, bikeType, date, company, region, tag)
                print('Store bike ' + bike['distId'],':',bike['distX'],',',bike['distY'])
            except sqlite3.IntegrityError as e:
                print('In ' + date + ' has crawl the bike ' + id + ' of ' + company + ',try update')
#updateDb(c, id, lng, lng, bikeType, date, company, region)
                
        conn.commit()
    except TypeError as e:
#print(e.args)
        print('Parse json TypeError')

def storeToDb(cursor, id, lng, lat, bikeType, date, company, region, tag):
    clause = 'INSERT INTO Bikes values(\'' \
        + id + '\',' + str(lng) + ',' + str(lat) + ',' + str(bikeType) + ',\'' \
        + date + '\',\'' + company + '\',\'' + region + '\',\'' + tag +'\')'
    #print(clause)
    cursor.execute(clause)
    
def updateDb(cursor, id, lng, lat, bikeType, date, company, region):
    clause = 'UPDATE Bikes SET (id, lng, lat, bikeType, date, company, region)' \
        + ' = ' + '(\'' + id + '\',' + str(lng) + ',' + str(lat) + ',' + str(bikeType) + ',\'' \
        + date + '\',\'' + company + '\',\'' + region + '\')' \
        + 'WHERE id=' + id
    #print(clause)
    cursor.execute(clause)
    
def getRegion(lat, lng):
    tmp = int(lat * 1000) / 1000
    lat = tmp
    tmp = int(lng * 1000) / 1000
    lng = tmp
    region = str(lat) + ',' + str(lng)
    return region
    

def makeRequest(lat, lng) :
    utcTime = int(time.time())
    localTime = int(utcTime * 1000)
    url = 'https://app.mobike.com/api/nearby/v3/nearbyBikeInfo'
    HEADERS = {
        'version': '6.9.0', 'versionCode': '1680', 'platform': '1', 
        'mainSource': '4002', 'subSource': '5', 'os': '25', 'lang': 'en', 
        'time': localTime, 'country': '0', 'eption': 'daf2b', 
        'deviceresolution': '1080X1920', 'utctime': utcTime, 
        'uuid': 'fc2567c5371315217a9abd7a57f45326', 
        'longitude': str(lng), 'latitude': str(lat), 
        'Content-Type': 'application/x-www-form-urlencoded', 
        'Content-Length': '144', 'Host': 'app.mobike.com', 
        'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip', 
        'User-Agent': 'okhttp/3.9.1'
    }

    DATA = ('scope=500&sign=edaf3f37e2343f2fe63ff85f156f66b4&client_id=android&biketype=0&longitude=' \
        +str(lng)+'67844588&latitude=' + str(lat) + '423412055&bikenum=50').encode('ascii')

    try:
        print('Request bikes at ' + str(lat) +','+ str(lng) + ' at ' +  str(datetime.datetime.today()))
        request = req.Request(url, data=DATA, headers=HEADERS, method='POST')
        html = req.urlopen(request)
        return html.read().decode('utf-8')
    except Exception as e:
        print('Network error..........')

def crawlRegion(origin, terminal, tag):
    originLatLng = origin
    terminalLatLng = terminal
    lat = originLatLng[0]
    lng = originLatLng[1]
    conn = sqlite3.connect('ShareBikes.db')
    while lat > terminalLatLng[0]:
        while lng < terminalLatLng[1]:
            parseJson(conn, makeRequest(lat, lng), 'mobike', tag)
            #time.sleep(1)
            lng += 0.0005
        lat -= 0.0005
        lng = originLatLng[1]
    conn.close()  


def main():
    tag = input('Please input the tag:')
    regions = [[[22.590715,113.884621],[22.518424,113.975601]],[[22.560281,113.975601],[22.519851,114.035168]],
        [[22.566147,114.029160],[22.516363,114.079285]],[[22.573755,114.072418],[22.531110,114.144516]],
        [[22.647126,114.100227],[22.598322,114.163399]],[[22.528097,113.885307],[22.479886,113.957062]]]
    for region in regions:
        crawlRegion(region[0], region[1], tag)
    
main()
#conn = sqlite3.connect('ShareBikesssss.db')
#parseJson(conn, makeRequest(22.540900,113.953714), 'mobike')
