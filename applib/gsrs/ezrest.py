import requests
import gsrs.config
import gsrs.logging
import traceback
import json
import gsrs.config

general_logger = gsrs.logging.get_logger('general')
request_logger = gsrs.logging.get_logger('request')
response_logger = gsrs.logging.get_logger('response')
summary_logger = gsrs.logging.get_logger('summary')

def get(url, id, **args):
    logStartMethod("GET")
    exceptions = []
    rc = ''
    try:
       response = requests.get(url, verify=False)
       if response.status_code:
          rc = response.status_code
       id  = "NOID" if id is None else id
       logResponse(response.content.decode())
    except Exception as e:
        response = None
        exceptions.append(str(e))
        logException(str(e))
        logTraceback(traceback.print_exc())
    log_string = "\t".join([id, rc, "|".join(exceptions)])
    general_logger.info(log_string)
    logEndMethod("GET")
    return response if response else None


def post(url, id, json_text, **args):
    logStartMethod("POST")
    exceptions = []
    rc = ''
    try:
       _headers={'Content-Type': 'application/json', 'auth-username': gsrs.config.config['auth_username'], 'auth-password': gsrs.config.config['auth_password'],  'charset': 'utf-8'}
       # json_loaded = json.loads(json_text)
       logRequest(json_text)
       response = requests.post(url, data=json_text, headers=_headers, verify=False)
       if response.status_code:
           rc = response.status_code
       id  = 'NOID' if id is None or id=='' else id
       logResponse(response.content.decode())
    except Exception as e:
        response = None
        exceptions.append(str(e))
        logException(str(e))
        logTraceback(traceback.print_exc())
    log_string = "\t".join([str(id), str(rc), "|".join(exceptions)])
    # general_logger.info(log_string)
    logEndMethod("POST")
    return response if response else None


def put(url, id, json_text, **args):
    logStartMethod("PUT")
    exceptions = []
    rc = ''
    try:
       _headers={'Content-Type': 'application/json', 'auth-username': gsrs.config.config['auth_username'], 'auth-password': gsrs.config.config['auth_password'],  'charset': 'utf-8'}
       # json_loaded = json.loads(json_text)
       logRequest(json_text)
       response = requests.put(url, data=json_text, headers=_headers, verify=False)
       if response.status_code:
          rc = response.status_code
       id  = "NOID" if id is None else id
       logResponse(response.content.decode())
    except Exception as e:
        response = None
        exceptions.append(str(e))
        logException(str(e))
        logTraceback(traceback.print_exc())
    log_string = "\t".join([str(id), str(rc), "|".join(exceptions)])
    general_logger.info(log_string)
    logEndMethod("PUT")
    return response if response else None


def delete(url, id, json_text, **args):
    logStartMethod("DELETE")
    exceptions = []
    rc = ''
    try:
       _headers={'Content-Type': 'application/json', 'auth-username': gsrs.config.config['auth_username'], 'auth-password': gsrs.config.config['auth_password'],  'charset': 'utf-8'}
       # json_loaded = json.loads(json_text)
       logRequest(json_text)
       response = requests.delete(url, data=json_text, headers=_headers, verify=False)
       if response.status_code:
          rc = response.status_code
       id  = 'NOID' if id is None else id
       logResponse(response.content.decode())
    except Exception as e:
        response = None
        exceptions.append(str(e))
        logException(str(e))
        logTraceback(traceback.print_exc())
    log_string = "\t".join([str(id), str(rc), "|".join(exceptions)])
    general_logger.info(log_string)
    logEndMethod("DELETE")
    return response if response else None


def printableLogString(label, value):
    return label + ': ' + noneOk(value)

def noneOk(value):
    value = '' if value is None else value
    return value


def logSummary(value):
    if gsrs.config.config['logging']['general']['summary'] and gsrs.config.config['logging']['summary']['request']==1:
        general_logger.info(printableLogString('Response', value))
    if gsrs.config.config['logging']['defined']['summary'] and gsrs.config.config['logging']['defined']['summary']==1:
        summary_logger.info(printableLogString('', value))

def logRequest(value):
    if gsrs.config.config['logging']['general']['request'] and gsrs.config.config['logging']['general']['request']==1:
        general_logger.info(printableLogString('Request', value))
    if gsrs.config.config['logging']['defined']['request'] and gsrs.config.config['logging']['defined']['request']==1:
        request_logger.info(printableLogString('Request', value))

def logResponse(value):
    if gsrs.config.config['logging']['general']['response'] and gsrs.config.config['logging']['response']['request']==1:
        general_logger.info(printableLogString('Response', value))
    if gsrs.config.config['logging']['defined']['response'] and gsrs.config.config['logging']['defined']['response']==1:
        response_logger.info(printableLogString('Response', value))

def logException(value):
    if gsrs.config.config['logging']['general']['exceptions'] and gsrs.config.config['logging']['general']['exceptions']==1:
        general_logger.info(printableLogString('Exception', value))

def logTraceback(value):
    if gsrs.config.config['logging']['general']['traceback'] and gsrs.config.config['logging']['general']['traceback']==1:
        general_logger.info(printableLogString('Traceback', value))

def logStartMethod(value):
    if gsrs.config.config['logging']['general']['startend'] and gsrs.config.config['logging']['general']['startend']==1:
      general_logger.info("=== Starting " + value + "===")

def logEndMethod(value):
    if gsrs.config.config['logging']['general']['startend'] and gsrs.config.config['logging']['general']['startend']==1:
        general_logger.info("=== Ending " + value + "===\n")
