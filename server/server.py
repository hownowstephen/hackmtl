from apy import Endpoint, app
from database import TransitDB
from yellowapi import YellowAPI
from time import time
from pprint import pprint
import json
import sys
import urllib
from unidecode import unidecode

db = TransitDB()
yapi = YellowAPI(api_key='z97y87jxuzctq583fnukert4', test_mode=True)

distance_calc = '( 3959 * acos( cos( radians({lat}) ) * cos( radians( lat ) ) * cos( radians( lng ) - radians({lng}) ) + sin( radians({lat}) ) * sin( radians( lat ) ) ) ) as distance'


@Endpoint('/destinations')
class nearby_metros:
    '''Basic example returns a json response'''

    def get(*args, **kwargs):
        '''Responds to a GET request'''
        try:
            lat, lng = float(kwargs['lat']), float(kwargs['lng'])
            return {'status': 'success', 'response': []}
        except:
            return {'status': 'failed', 'reason': 'could not retrieve your location'}


@Endpoint('/taxis')
class Taxis:

    def get(*args, **kwargs):
        try:
            if not 'location' in kwargs:
                kwargs['location'] = 'cZ%s,%s' % (float(kwargs['lng']), float(kwargs['lat']))

            for taxi in json.loads(yapi.find_business('taxi', kwargs['location'], time(), page_len=1))['listings']:
                pprint(taxi)
                try:
                    print yapi.get_business_details('', '', taxi['id'], time())
                except:
                    from traceback import print_tb
                    print sys.exc_info()
                    print_tb(sys.exc_info()[2])
                break

            return {'status': 'success', 'response': []}

        except:
            print sys.exc_info()
            return {'status': 'failed', 'reason': 'could not retrieve your location'}


def cache_taxis():
    for taxi in json.loads(yapi.find_business('taxi', 'montreal', time(), page_len=100))['listings']:

        if taxi['geoCode']:
            lat, lng = taxi['geoCode']['latitude'], taxi['geoCode']['longitude']
            try:
                sql = "INSERT INTO taxis (lat, lng, yid, name) VALUES (%s, %s, %s, '%s');" % (lat, lng, taxi['id'], urllib.quote(unidecode(taxi['name'])))
                db.cursor.execute(sql)
                db.conn.commit()
            except:
                pass
            print 'added taxi at %s,%s' % (lat, lng)
cache_taxis()

app.debug = True
if __name__ == '__main__':
    app.run()
