import re
import json
from sqlite3 import Timestamp
import numpy as np
from datetime import date, timedelta, datetime, timezone
import pandas as pd
import pytz

AZURE_TABLES_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

# handling JOSON serialization fo datetime objects
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, np.int64): 
        try:
            return int(obj)
        except:
            return "NaN"
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    else:
        try:
            return obj.__dict__
        except:
            raise TypeError ("Type %s not serializable" % type(obj)) 

def read_json_from_bytes(bytes):
	'''converts a bytes array into a Json'''
	my_json = bytes.decode('utf8')
	return json.loads(my_json)

# DATETIME utilities
def to_datetime(date_object):
    '''tries its best to convert anythinkg into a datetime object in the likes of this: 2021-05-19 02:00:00+02:00
    this does not deal with timezones, if your datetime object/string is naive, then the result will be naive too'''
    if isinstance(date_object, pd.Timestamp):
        return timestamp_to_datetime(date_object)
    if isinstance(date_object, datetime):
        return date_object
    elif isinstance(date_object, str):
        try:
            return timestamp_to_datetime(pd.to_datetime(date_object))
        except:
            raise ValueError('Unable to parse ' + str(date_object) + ' into a datetime object.')

def to_tz_aware_datetime(date_string, timezone=pytz.utc, fallback ='None'):
    '''read dates and fails silently, returns a TZ aware datetime. Good for parsing anything that
    may be a datetime, like an input parameter or whaterver shit the storage throws at you'''
    try:
        if isinstance(timezone, pytz.BaseTzInfo):
            return denaive_datetime(to_datetime(date_string), timezone)
        else:
            return denaive_datetime(to_datetime(date_string), pytz.timezone(timezone))  
    except  Exception as ex:
        # time to fail silently
        if fallback is not None:
            return fallback
        else:
            # or to yell at failure
            raise ex

def timestamp_to_datetime(timestamp, fallback=None):
    '''converts Pandas timestamp into a datetime.datetime object'''
    if isinstance(timestamp, Timestamp):
        try:
            out = timestamp.to_pydatetime()
            if pd.isnull(out):
                return fallback
            return out
        except:
            # fail silently
            return fallback
    # if it's aready ok do nothing
    elif isinstance(timestamp, datetime):
        return timestamp
    
   
    
def denaive_datetime(d, timezone = pytz.utc):
    '''turns a naive datime into a timezone-aware one, if the object is already TZ aware, it does nothing'''
    if (d.tzinfo is None) or (d.tzinfo.utcoffset(d) is None):
        return d.replace(tzinfo=timezone)
    else:
        # in this branch the datetime object is already TZ-aware hence do nothing
        return d
    

def datetime_to_tables_string(date_object):
    return date_object.strftime(AZURE_TABLES_DATETIME_FORMAT)


# GEO formats utils

def get_lat_lon_from_wkt(geom_string):
  # we have to parse this POINT (Lon Lat)
  try:
    m = re.search(r'(\d+\.?\d*)\s+(\d+\.?\d*)', geom_string)
    lon = m.group(1)
    lat = m.group(2)
    return lon, lat
  except:
    return None, None

def unfuck_numpy_formats(object):
    '''values that come out of NetCDF files are not in native Python types, but wrapped in numpy weirdness.
    We have to fix it otherwise Azure Tables will throw weird ass errors about malformed tuples'''
    if isinstance(object, np.generic): 
        return object.item()
    else:
        return object
