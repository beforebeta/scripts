import math

from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

import requests
from geopy.distance import distance as geopy_distance
import json

INCREMENT_MI = 5.0 # mile(s)
GROUPON_KEY = 'cd4f46230f4d6bb2c8467c1695e891f24a0baf37'
GROUPON_API_URL = 'http://api.groupon.com/v2/deals'

COLLECTED_DEALS = []

request_parameters = {
        'client_id': GROUPON_KEY,
        # 'radius': INCREMENT_MI
}

# denver bounding box: http://isithackday.com/geoplanet-explorer/index.php?woeid=24701640
north_east = Point(-103.705704,40.284950)
south_west = Point(-105.927017,39.128181)

x_dist_mi = geopy_distance((north_east.y, north_east.x), (north_east.y, south_west.x)).miles
y_dist_mi = geopy_distance((north_east.y, north_east.x), (south_west.y, north_east.x)).miles

x_grid_divisor = x_dist_mi / INCREMENT_MI
y_grid_divisor = y_dist_mi / INCREMENT_MI

x_increment_pnt = (north_east.x - south_west.x) / x_grid_divisor
y_increment_pnt = (north_east.y - south_west.y) / y_grid_divisor

x_move_count = int(math.ceil(x_grid_divisor)) + 1
y_move_count = int(math.ceil(y_grid_divisor)) + 1

# starting from south_west corner and move right across first, and move up
request_parameters['lat'] = south_west.y
request_parameters['lng'] = south_west.x
request_parameters['radius'] = 5
#request_parameters['division_id'] = 'colorado-springs'

lat_longs = []
for idx_y, y in enumerate(range(y_move_count)):
    for idx_x, x in enumerate(range(x_move_count)):
        print 'fetching.. row {} out of {} : column {} out of {} >> lat:{}, lng:{})'.format(idx_y, y_move_count, idx_x, x_move_count, request_parameters['lat'], request_parameters['lng'])
        #lat_longs.append([request_parameters['lat'], request_parameters['lng']])
        deals = requests.get(GROUPON_API_URL, params=request_parameters).json()['deals']
        COLLECTED_DEALS.extend(deals)
        print "deals returned", len(deals)
        print "unique deals", len(set([d["uuid"] for d in COLLECTED_DEALS]))
        print "total deals", len(COLLECTED_DEALS)
        request_parameters['lng'] += x_increment_pnt
    request_parameters['lng'] = south_west.x
    request_parameters['lat'] += y_increment_pnt
COLLECTED_DEALS_IDS = [d['uuid'] for d in COLLECTED_DEALS]
print "Total unique deals collected:", len(set(COLLECTED_DEALS_IDS))

#print json.dumps(lat_longs)