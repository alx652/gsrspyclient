import requests
import plugins.clinicaltrialsus.mapper
import json
import plugins.clinicaltrialsus.functions
from io import StringIO  
import csv
from datetime import datetime
from gsrs.dire import * 

# linux
# csv.field_size_limit(sys.maxsize)
# windows
csv.field_size_limit(2147483647)


mapperInstance = plugins.clinicaltrialsus.mapper.Mapper()
fm = mapperInstance.fieldMap 

def bulkDownloadTrialsByPage(csv_file): 
  pageSize=1000
  pageTokenQs = ''
  totalCount = None;
  finished = False
  csvFields = []
  urlTemplate = "https://clinicaltrials.gov/api/v2/studies?format=csv&countTotal=true&pageSize={0}{1}"
  i=0
  with open(csv_file, 'w', newline='', encoding="utf-8") as file:
    while(not finished):
      i=i+1
      warn("Getting up to " +  str(pageSize) +" records, up to total "+ str(i*pageSize))
      urlFormatted = urlTemplate.format(pageSize, pageTokenQs)
      response = requests.get(urlFormatted)
      if (i==1 and ('x-total-count' in response.headers)):    
        totalCount = response.headers['x-total-count']
        csvFields =  response.text.partition('\n')[0].strip().split("\t")
      file.write(response.text)
      if 'x-next-page-token' in response.headers:    
        pageTokenQs = '&pageToken=' + response.headers['x-next-page-token']  
      else:
        finished = True
#      if i>10:    
#        finished = True

def extractIdsFromCsvFile(csv_file): 
  with open(csv_file, 'r', newline='', encoding="utf-8") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        print(row['NCT Number'])

def getSingleTrialAsCsvText(trialNumber): 
  urlTemplate = 'https://clinicaltrials.gov/api/v2/studies/{0}?format=csv&markupFormat=legacy'
  urlFormatted = urlTemplate.format(trialNumber)
  response = requests.get(urlFormatted)
  # rather than response.text because windows  
  return response.content.decode('utf-8')

def makeCsvDictFromTrialCsvText(csvText):
  file = StringIO(csvText)
  csv_reader = csv.DictReader(file)
  trial = next(csv_reader)
  return trial

def makeGsrsDictFromTrialCsvText(csvText):
  trial = makeCsvDictFromTrialCsvText(csvText)
  return makeGsrsTrialDictFromCsvDict(trial)

def makeGsrsTrialDictFromCsvDict(trial):
  d = dict()
  for key in fm.keys():
    if 'gsrsName' in fm[key] and fm[key]['gsrsName'] is not None and fm[key]['gsrsName'].strip() != '':
      if fm[key]['type'] == 'date':
        d[fm[key]['gsrsName']] = plugins.clinicaltrialsus.functions.makeMillisFromClinicalTrialsGovDateString(trial[key])
      else:
        if (fm[key]['length'] in fm[key] and fm[key]['length'].isnumeric() and fm[key]['length']> 0): 
          d[fm[key]['gsrsName']] = trial[key][:fm[key]['length']]
        else:
          d[fm[key]['gsrsName']] = trial[key]
  return d  

def getGsrsTrialAsDict(trialNumber):
  d = dict()
  file = StringIO(csvText)
  csv_reader = csv.DictReader(file)
  trial = next(csv_reader)
  for key in fm.keys():
      if 'gsrsName' in fm[key] and fm[key]['gsrsName'] is not None and fm[key]['gsrsName'].strip() != '': 
          d[fm[key]['gsrsName']] = trial[key]
  return d


def skipPutWhenLastUpdateDatesEqual(gsrsDate, csvDate):
  try: 
    csvDateAsMillis = plugins.clinicaltrialsus.functions.makeMillisFromClinicalTrialsGovDateString(csvDate)
    if (gsrsDate == csvDateAsMillis): 
      return True
  except Exception as e:
      return False
  

 