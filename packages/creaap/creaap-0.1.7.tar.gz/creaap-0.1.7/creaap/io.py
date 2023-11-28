import base64
import json
import math
import numpy as np
from datetime import date, timedelta, datetime, timezone
import pandas as pd
import pytz

from creaap.formats import to_tz_aware_datetime


# handling JSON serialization fo datetime objects
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if type(obj) is float and math.isnan(obj):
        return "NaN"
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

def get_parameter_with_default(req, par_name, default_val = None):
	value = req.params.get(par_name)
	if not value:
		try:
			req_body = req.get_json()
		except ValueError:
			value = default_val
		else:
			value = req_body.get(par_name)
			if not value:
				value = default_val
	return value

def get_parameter(req, par_name):
	value = req.params.get(par_name)
	if not value:
		try:
			req_body = req.get_json()
		except ValueError:
			pass
		else:
			value = req_body.get(par_name)
	return value

def get_datetime_parameter_with_default(req, par_name, default_val, timezone_par = 'timezone', target_timezone = 'utc', **kwargs):
	val = get_parameter_with_default(req, par_name, default_val = None)
	tz = get_parameter_with_default(req, timezone_par, default_val = None)
	if val:
		try:
			return to_tz_aware_datetime(val, origin_timezone = tz, target_timezone= target_timezone, **kwargs)
		except:
			return default_val
	return default_val


