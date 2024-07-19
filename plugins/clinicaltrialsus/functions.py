from datetime import datetime, timezone, timedelta
from dateutil import parser

import re

def normalizeDateSeparator(dateString):
    if dateString is not None: 
        parts = re.split('[-/]', dateString)
        return '/'.join(parts)
    else:
        return None        

def blankIfNull(s): 
    if s is None:
        return ''
    return s

def blankIfNullAndTrim(s): 
    if s is None:
        return ''       
    return s.strip()



def use_later_datetimeToEpochMillis(dt):
    # this doesn't work on windows if date is less than 1970-01-01
    return (int(dt.timestamp() * 1000))

def datetimeToEpochMillis(dt):
    ts = int((dt-datetime(1970,1,1)).total_seconds()*1000)
    return ts

def makeDateFromYearMonthDayString(dateString):
    try:
        d = datetime.strptime(dateString,"%Y/%m/%d")
        return d
    except: 
        return None

def makeDateFromYearMonthString(dateString):
    try:
        d = datetime.strptime(dateString,"%Y/%m")
        return d
    except: 
        return None

def makeDateFromMonthDayYearString(dateString):
    try:
        d = datetime.strptime(dateString,"%m/%d/%Y")
        return d
    except: 
        return None

def makeDateFromMonthYearString(dateString):
    try:
        d = datetime.strptime(dateString,"%m/%Y")
        return d
    except: 
        return None


def makeMillisFromClinicalTrialsGovDateString(dateString):
    ds =  normalizeDateSeparator(dateString)
    d = makeDateFromYearMonthDayString(ds)
    if d is not None:
        return datetimeToEpochMillis(d)
    d = makeDateFromYearMonthString(ds)
    if d is not None:
        return datetimeToEpochMillis(d)
    return 0



