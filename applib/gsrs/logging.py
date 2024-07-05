import logging
import sys
# from logging.handlers import TimedRotatingFileHandler, 
from datetime import datetime
import gsrs.config 

# https://www.toptal.com/python/in-depth-python-logging

startTime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

FORMATTER = logging.Formatter("%(message)s")
GENERAL_LOG_FILE = 'data/logs/'+ startTime +'-general.log'
ADHOC_LOG_FILE = 'data/logs/'+ startTime +'-adhoc.log'
REQUEST_LOG_FILE = 'data/logs/'+ startTime +'-request.log'
RESPONSE_LOG_FILE = 'data/logs/'+ startTime +'-response.log'

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler

def get_file_handler():
   # file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight', encoding='utf8')
   file_handler = logging.FileHandler(GENERAL_LOG_FILE, mode='w', encoding='utf8')
   file_handler.setFormatter(FORMATTER)
   return file_handler

def get_response_file_handler():
   file_handler = logging.FileHandler(RESPONSE_LOG_FILE, mode='w', encoding='utf8')
   file_handler.setFormatter(FORMATTER)
   return file_handler

def get_request_file_handler():
   file_handler = logging.FileHandler(REQUEST_LOG_FILE, mode='w', encoding='utf8')
   file_handler.setFormatter(FORMATTER)
   return file_handler

def get_adhoc_file_handler():  
   file_handler = logging.FileHandler(ADHOC_LOG_FILE, mode='w', encoding='utf8')
   file_handler.setFormatter(FORMATTER)
   return file_handler

def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG)
   if logger_name == 'general':
      logger.addHandler(get_console_handler())
      logger.addHandler(get_file_handler())
   if logger_name == 'request':
      logger.addHandler(get_request_file_handler())
   if logger_name == 'response':
      logger.addHandler(get_response_file_handler())
   if logger_name == 'adhoc':
      logger.addHandler(get_adhoc_file_handler())         
   logger.propagate = False
   return logger

def noneOk(value):
    value = '' if value is None else value
    return value

def printableLogString(label, value):
   if label is None or label == '': 
      return  noneOk(value)
   else: 
      return label + ': ' + noneOk(value)

def logAdhoc(value):
    if gsrs.config.config['logging']['general']['adhoc'] and gsrs.config.config['logging']['general']['adhoc']==1:
        adhoc_logger.info(noneOk(value))

def logStandard(value):
    if gsrs.config.config['logging']['general']['standard'] and gsrs.config.config['logging']['general']['standard']==1:
        general_logger.info(printableLogString(None, value))

def logRequest(value):
    if gsrs.config.config['logging']['general']['request'] and gsrs.config.config['logging']['general']['request']==1:
        general_logger.info(printableLogString('Request', value))
    if gsrs.config.config['logging']['defined']['request'] and gsrs.config.config['logging']['defined']['request']==1:
        request_logger.info(printableLogString('Request', value))

def logResponse(value):
    if gsrs.config.config['logging']['general']['response'] and gsrs.config.config['logging']['general']['response']==1:
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


adhoc_logger = get_logger('adhoc')
general_logger = get_logger('general')
request_logger = get_logger('request')
response_logger = get_logger('response')

