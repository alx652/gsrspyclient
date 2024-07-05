import requests
import gsrs.config
import gsrs.logging
import traceback
import json
import gsrs.config

def get(url, id, **args):
    gsrs.logging.logStartMethod("GET")
    exceptions = []
    rc = ''
    try:
       response = requests.get(url, verify=False)
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
    exceptions = []
    rc = ''
    try:
       _headers={'Content-Type': 'application/json', 'auth-username': gsrs.config.config['auth_username'], 'auth-password': gsrs.config.config['auth_password'],  'charset': 'utf-8'}
       # json_loaded = json.loads(json_text)
       gsrs.logging.logRequest(json_text)
       response = requests.post(url, data=json_text, headers=_headers, verify=False)
       if response.status_code:
           rc = response.status_code
       id  = 'NOID' if id is None or id=='' else id
       gsrs.logging.logResponse(response.content.decode())
    except Exception as e:
        response = None
        exceptions.append(str(e))
        logException(str(e))
        logTraceback(traceback.print_exc())
    log_string = "\t".join([str(id), str(rc), "|".join(exceptions)])
    gsrs.logging.logStandard(log_string)
    gsrs.logging.logEndMethod("POST")
    return response


def put(url, id, json_text, **args):
    gsrs.logging.logStartMethod("PUT")
    exceptions = []
    rc = ''
    try:
       _headers={'Content-Type': 'application/json', 'auth-username': gsrs.config.config['auth_username'], 'auth-password': gsrs.config.config['auth_password'],  'charset': 'utf-8'}
       # json_loaded = json.loads(json_text)
       gsrs.logging.logRequest(json_text)
       response = requests.put(url, data=json_text, headers=_headers, verify=False)
       if response.status_code:
          rc = response.status_code
       id  = "NOID" if id is None else id
       gsrs.logging.logResponse(response.content.decode())
    except Exception as e:
        response = None
        exceptions.append(str(e))
        logException(str(e))
        logTraceback(traceback.print_exc())
    log_string = "\t".join([str(id), str(rc), "|".join(exceptions)])
    gsrs.logging.logStandard(log_string)
    gsrs.logging.logEndMethod("PUT")
    return response
    

def delete(url, id, json_text, **args):
    logStartMethod("DELETE")
    exceptions = []
    rc = ''
    try:
       _headers={'Content-Type': 'application/json', 'auth-username': gsrs.config.config['auth_username'], 'auth-password': gsrs.config.config['auth_password'],  'charset': 'utf-8'}
       # json_loaded = json.loads(json_text)
       gsrs.logging.logRequest(json_text)
       response = requests.delete(url, data=json_text, headers=_headers, verify=False)
       if response.status_code:
          rc = response.status_code
       id  = 'NOID' if id is None else id
       gsrs.logging.logResponse(response.content.decode())
    except Exception as e:
        response = None
        exceptions.append(str(e))
        logException(str(e))
        logTraceback(traceback.print_exc())
    log_string = "\t".join([str(id), str(rc), "|".join(exceptions)])
    gsrs.logging.logStandard(log_string)
    gsrs.logging.logEndMethod("DELETE")
    return response