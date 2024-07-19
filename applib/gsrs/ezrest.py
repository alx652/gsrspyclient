import requests
import gsrs.config
import gsrs.logging
import traceback
import json
import gsrs.config
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def get(url, id, **args):
    _headers = {
        'auth-username': gsrs.config.get_auth_username(), 
        gsrs.config.get_auth_method(): gsrs.config.get_auth_method_value(),
        'charset': 'utf-8'
    }
    gsrs.logging.logStartMethod("GET")
    exceptions = []
    rc = ''
    try:
       warnings.simplefilter('ignore', InsecureRequestWarning)
       response = requests.get(url, headers=_headers, verify=False, timeout=60)
       if response.status_code:
          rc = response.status_code
       id  = "NOID" if id is None else id
       gsrs.logging.logResponse(response.content.decode())
    except Exception as e:
        response = None
        exceptions.append(str(e))
        gsrs.logging.logException(str(e))
        gsrs.logging.logTraceback(traceback.print_exc())
    log_string = "\t".join([id, str(rc), "|".join(exceptions)])
    gsrs.logging.logStandard(log_string)
    gsrs.logging.logEndMethod("GET")
    return response


def post(url, id, json_text, **args):
    gsrs.logging.logStartMethod("POST")
    _headers = {
        'Content-Type': 'application/json',
        'auth-username': gsrs.config.get_auth_username(), 
        gsrs.config.get_auth_method(): gsrs.config.get_auth_method_value(),
        'charset': 'utf-8'
    }
    exceptions = []
    rc = ''
    try:
       gsrs.logging.logRequest(json_text)
       warnings.simplefilter('ignore', InsecureRequestWarning)
       response = requests.post(url, data=json_text, headers=_headers, verify=False, timeout=60)
       if response.status_code:
           rc = response.status_code
       id  = 'NOID' if id is None or id=='' else id
       gsrs.logging.logResponse(response.content.decode())
    except Exception as e:
        response = None
        exceptions.append(str(e))
        gsrs.logging.logException(str(e))
        gsrs.logging.logTraceback(traceback.print_exc())
    log_string = "\t".join([str(id), str(rc), "|".join(exceptions)])
    gsrs.logging.logStandard(log_string)
    gsrs.logging.logEndMethod("POST")
    return response


def put(url, id, json_text, **args):
    gsrs.logging.logStartMethod("PUT")
    _headers = {
        'Content-Type': 'application/json',
        'auth-username': gsrs.config.get_auth_username(), 
        gsrs.config.get_auth_method(): gsrs.config.get_auth_method_value(),
        'charset': 'utf-8'
    }
    exceptions = []
    rc = ''
    try:
       gsrs.logging.logRequest(json_text)
       warnings.simplefilter('ignore', InsecureRequestWarning)
       response = requests.put(url, data=json_text, headers=_headers, verify=False, timeout=60)
       if response.status_code:
          rc = response.status_code
       id  = "NOID" if id is None else id
       gsrs.logging.logResponse(response.content.decode())
    except Exception as e:
        response = None
        exceptions.append(str(e))
        gsrs.logging.logException(str(e))
        gsrs.logging.logTraceback(traceback.print_exc())
    log_string = "\t".join([str(id), str(rc), "|".join(exceptions)])
    gsrs.logging.logStandard(log_string)
    gsrs.logging.logEndMethod("PUT")
    return response
    

def delete(url, id, json_text, **args):
    _headers = {
        'Content-Type': 'application/json',
        'auth-username': gsrs.config.get_auth_username(), 
        gsrs.config.get_auth_method(): gsrs.config.get_auth_method_value(),
        'charset': 'utf-8'
    }
    gsrs.logging.logStartMethod("DELETE")
    exceptions = []
    rc = ''
    try:
       gsrs.logging.logRequest(json_text)
       warnings.simplefilter('ignore', InsecureRequestWarning)
       response = requests.delete(url, data=json_text, headers=_headers, verify=False, timeout=60)
       if response.status_code:
          rc = response.status_code
       id  = 'NOID' if id is None else id
       gsrs.logging.logResponse(response.content.decode())
    except Exception as e:
        response = None
        exceptions.append(str(e))
        gsrs.logging.logException(str(e))
        gsrs.logging.logTraceback(traceback.print_exc())
    log_string = "\t".join([str(id), str(rc), "|".join(exceptions)])
    gsrs.logging.logStandard(log_string)
    gsrs.logging.logEndMethod("DELETE")
    return response    

def get_count_by_entity(entity):
    urlTemplate = gsrs.config.get_base_url() + entity +'/@count'
    getUrl = urlTemplate.format()
    args = {}
    getResponse = gsrs.ezrest.get(getUrl, '', **args)
    if (getResponse.status_code == 200):
        return int(getResponse.text.strip())
    return None

def get_count_by_indexed_entity(entity):
    urlTemplate = gsrs.config.get_base_url() + entity +'/search?top=0&skip=0'
    getUrl = urlTemplate.format()
    args = {}
    getResponse = gsrs.ezrest.get(getUrl, '', **args)
    if (getResponse.status_code == 200):
        return int(json.loads(getResponse.text)['total'])
    return None



def get_id_strings_by_entity(entity, page_size=500, max_pages=999999999):
    skip=0
    # repositoryCount = gsrs.ezrest.get_gsrs_count_by_entity(entity)
    repositoryCount = 1000
    trialsTally = 0
    pagesTally = 0
    ids = []
    args = {}
    print("here0")
    if (not (repositoryCount is None)):   
        urlTemplate = gsrs.config.get_base_url() + '{0}?view=key&top={1}&skip={2}'
        while (pagesTally < max_pages and trialsTally < repositoryCount): 
            pagesTally = pagesTally + 1
            print("here1")
            getUrl = urlTemplate.format(entity, page_size, skip)
            skip = skip + page_size
            getResponse = gsrs.ezrest.get(getUrl, '', **args)
            print("here2")
            dict = json.loads(getResponse.content.decode('utf-8'))
            trialsTally = trialsTally + dict['count']
            print("here3")
            ids.extend([i['idString'] for i in dict['content']])
            print("here4")
        return ids
    return None

def get_gsrs_id_strings_by_indexed_entity(entity, page_size=500, max_pages=999999999):
    skip=0
    repositoryCount = gsrs.ezrest.get_gsrs_count_by_entity(entity)
    trialsTally = 0
    pagesTally = 0
    ids = []
    args = {}
    if (not (repositoryCount is None)):   
        urlTemplate = gsrs.config.get_base_url() + '{0}/search?simpleSearchOnly=true&view=key&top={1}&skip={2}'
        while (pagesTally < max_pages and trialsTally <= repositoryCount): 
            pagesTally = pagesTally + 1
            getUrl = urlTemplate.format(entity, page_size, skip)
            skip = skip + page_size
            getResponse = gsrs.ezrest.get(getUrl, '', **args)
            dict = json.loads(getResponse.content.decode('utf-8'))
            trialsTally = trialsTally + dict['count']
            ids.extend([i['idString'] for i in dict['content']])
        return ids
    return None
