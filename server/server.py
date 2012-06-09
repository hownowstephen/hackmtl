from apy import Endpoint, app
from database import TransitDB
from yellowapi import YellowAPI
from time import time
import json
import sys
from unidecode import unidecode
from traceback import print_tb
import re
import txml
import requests

db = TransitDB()
yapi = YellowAPI(api_key='vvpw2zjmmp4t96xtkmt9xu8u', test_mode=True)

distance_calc = '( 3959 * acos( cos( radians({lat}) ) * cos( radians( lat ) ) * cos( radians( lng ) - radians({lng}) ) + sin( radians({lat}) ) * sin( radians( lat ) ) ) ) as distance'


@Endpoint('/bixi/<bixi_id>/')
class Bixi:

    def get(*args, **kwargs):

        try:
            parser = txml.Xml2Obj()
            element = parser.Parse(unidecode(requests.get("https://montreal.bixi.com/data/bikeStations.xml").content))
            for bixi in element.children:
                b = bixi.to_dict()
                if b['terminalName'].strip() == kwargs['bixi_id'].strip():
                    return {
                        'status': 'success',
                        'result': {
                            'name': b['name'],
                            'bikes': b['nbBikes'],
                            'docks': b['nbEmptyDocks'],
                            'lat': b['lat'],
                            'lng': b['long']
                        }
                    }
            raise
        except:
            print sys.exc_info()
            return {'status': 'failed', 'reason': 'bixi service unavailable'}


@Endpoint('/bixis')
class Bixis:

    def get(*args, **kwargs):

        try:
            distance = distance_calc.format(lat=float(kwargs['lat']), lng=float(kwargs['lng']))
            bixis = []
            for bixi in db.get_all("SELECT stat_name, terminalName, %s FROM bixi ORDER BY distance ASC limit 10" % distance):
                bixis.append({'name': bixi[0], 'code': bixi[1], 'distance': bixi[2]})
            return {'status': 'success', 'result': bixis}
        except:
            return {'status': 'failed', 'reason': 'no metro with that id found'}


@Endpoint('/metro/<metro_id>/')
class Metro:
    '''Returns details about a single metro'''

    def get(*args, **kwargs):

        try:
            stops = []
            for stop in db.get_all("SELECT arrival_time FROM stop_times WHERE stop_id='%s'" % kwargs['metro_id']):
                stops.append({'arrives': stop[0]})
            return {'status': 'success', 'results': stops}
        except:
            return {'status': 'failed', 'reason': 'no metro with that id found'}


@Endpoint('/metros')
class Metros:
    '''Basic example returns a json response'''

    def get(*args, **kwargs):
        '''Responds to a GET request'''
        try:
            distance = distance_calc.format(lat=float(kwargs['lat']), lng=float(kwargs['lng']))
            metros = []
            for metro in db.get_all("SELECT stop_name, stop_code, %s FROM stops ORDER BY distance ASC limit 10" % distance):
                metros.append({'name': metro[0], 'code': metro[1], 'distance': metro[2]})
            return {'status': 'success', 'response': metros}
        except:
	    print sys.exc_info()
            return {'status': 'failed', 'reason': 'could not retrieve your location'}


@Endpoint('/taxis')
class Taxis:

    def get(*args, **kwargs):
        try:
            distance = distance_calc.format(lat=float(kwargs['lat']), lng=float(kwargs['lng']))
            taxi = db.get_one("SELECT yid, name, lat, lng, phone, %s FROM taxis ORDER BY distance ASC LIMIT 3" % distance)
            if not taxi[4]:
                details = (yapi.get_business_details('QC', taxi[1], taxi[0], time()))
                details = json.loads(details)
                phone = details['phones'][0]['dispNum']
                db.run("UPDATE taxis SET phone='%s' WHERE yid='%s'" % (phone, taxi[0]))
            else:
                phone = taxi[4]

            return {
                'status': 'success',
                'results': {
                    'name': taxi[1].replace('-', ' '),
                    'phone': phone,
                    'lat': taxi[2],
                    'lng': taxi[3]
                }
            }
        except:
            print sys.exc_info()
            print_tb(sys.exc_info()[2])
            return {'status': 'failed', 'reason': 'could not retrieve your location'}


def cache_taxis():
    for taxi in json.loads(yapi.find_business('taxi', 'montreal', time(), page_len=100))['listings']:

        if taxi['geoCode']:
            lat, lng = taxi['geoCode']['latitude'], taxi['geoCode']['longitude']
            try:
                sql = "INSERT INTO taxis (lat, lng, yid, name) VALUES (%s, %s, %s, '%s');" % (lat, lng, taxi['id'], re.sub('[^\da-zA-Z]', '-', unidecode(taxi['name'])))
                db.cursor.execute(sql)
                db.conn.commit()
            except:
                pass
            print 'added taxi at %s,%s' % (lat, lng)

app.debug = True
if __name__ == '__main__':
    app.run(host='50.57.65.176')
