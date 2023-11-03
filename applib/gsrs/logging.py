import logging
import sys
# from logging.handlers import TimedRotatingFileHandler, 
from datetime import datetime

# https://www.toptal.com/python/in-depth-python-logging

startTime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

FORMATTER = logging.Formatter("%(message)s")
GENERAL_LOG_FILE = 'data/logs/'+ startTime +'-general.log'
SUMMARY_LOG_FILE = 'data/logs/'+ startTime +'-summary.log'
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

def get_summary_file_handler():  
   file_handler = logging.FileHandler(SUMMARY_LOG_FILE, mode='w', encoding='utf8')
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
   if logger_name == 'summary':
      logger.addHandler(get_summary_file_handler())         
   logger.propagate = False
   return logger
