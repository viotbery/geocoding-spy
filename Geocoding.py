# -*- coding: utf-8 -*-


import requests
from urllib.parse import urlencode
import json
import string
import coordtransf

Geocoding_URL = 'https://restapi.amap.com/v3/geocode/geo?'
Geocoding_API = 'your key'


def coding( address ):
    params = {
        'key': Geocoding_API,
        'address': address,
    }
    return requests.get(Geocoding_URL, params)


def getcoord(address):
    res = json.loads(coding(address).content)
    if res.get('status') == '1':
        coordstr = res.get('geocodes')[0].get('location')
        coordlist = coordstr.split(',')
        coord = (float(coordlist[0]), float(coordlist[1]))
        WGS_coord = coordtransf.gcj02_to_wgs84(coord[0], coord[1])
        return WGS_coord
    else :
        return [None, None]

if __name__ == '__main__':
    coord = getcoord('文化部')
    if coord[0] or coord[1]:
        print('yes')
    print(coord)
    print('lng :', coord[0], '\nlat :', coord[1])
    
