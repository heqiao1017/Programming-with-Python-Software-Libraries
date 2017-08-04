#A module that interacts with the Open MapQuest APIs.
#This is where you should do things like building URLs,
#making HTTP requests, and parsing JSON responses.

import json
import urllib.request
import urllib.parse

MAPQUEST_API_KEY='wLAbzAL9QfgHH9B9XpKXLAqdjCbqlvMB'

BASE_MAPQUEST_DIRECTION_URL='http://open.mapquestapi.com/directions/v2/route?'
BASE_MAPQUEST_ELEVATION_URL='http://open.mapquestapi.com/elevation/v1/profile?'

def build_direction_url(address_query:[])->str:
    query_parameter=[
        ('key',MAPQUEST_API_KEY),
        ('from',address_query[0])
        ]
    
    for address in address_query:
        if address!=address_query[0]:
            query_parameter.append(('to',address))

    return BASE_MAPQUEST_DIRECTION_URL+urllib.parse.urlencode(query_parameter)
        
def build_elevation_urls(lat_lng_collection:[[]])->[]:
    url_list=[]
    lat_lng_data=''
    for lat_lng in lat_lng_collection:
        for item in lat_lng:
            lat_lng_data+=str(item)
            lat_lng_data+=','
        url=BASE_MAPQUEST_ELEVATION_URL+'key='+MAPQUEST_API_KEY+'&latLngCollection='+lat_lng_data[:-1]
        url_list.append(url)
        lat_lng_data=''

    return url_list

def get_json_result(url:str)->dict:
    response=None
    try:
        response = urllib.request.urlopen(url)
        json_text=response.read().decode(encoding='utf-8')
        return json.loads(json_text)
    finally:
        if response!=None:
            response.close()
    
