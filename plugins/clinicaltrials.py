import os
import sys
sys.path.append('lib')
sys.path.append('./')
import json
import click
import csv

import gsrs.ezrest
import gsrs.config
import gsrs.click
import gsrs.utils

import plugins.clinicaltrialsus.test 


from ppretty import ppretty
from datetime import datetime

import gsrs.logging


class Plugin:
    def __init__(self, *args, **kwargs):
        pass

    def clinicaltrials(self, list):
        pass

## This is not part of class.
## CLI commands specific to clinicaltrialsgroup

@click.group()
def clinicaltrialsgroup():
    pass

@clinicaltrialsgroup.group()
def clinicaltrials():
    pass

@clinicaltrials.command(help="Pipe in, or enter list of names or ids followed by Ctrl-D")
def update_meta_data():
    trialNumber='NCT00132639'
    plugin = Plugin()
    url = gsrs.config.get_base_url() + 'clinicaltrialsus/' + trialNumber
    args = {}
    t1 = datetime.now()
    response = gsrs.ezrest.get(url, **args)
    print(response.text)


@clinicaltrials.command(help="Pipe in, or enter list of names or ids followed by Ctrl-D")
@click.argument('trial-number', nargs=1)
def post_trial_meta(trial_number):
    trialCsvText = plugins.clinicaltrialsus.test.getSingleTrialAsCsvText(trial_number)
    trialDict =  plugins.clinicaltrialsus.test.makeDictFromTrialCsvText(trialCsvText)
    plugin = Plugin()
    url = gsrs.config.get_base_url() + 'clinicaltrialsus'
    args = {}
    response = gsrs.ezrest.post(url, trial_number, json.dumps(trialDict, indent=2), **args)

"""
stages
     csv 
       response
          status_code: 200
          decoded 
          encoded
       exceptions 

    gsrs get
       response
          status_code: 200
          decoded
       exceptions 

     gsrs persist 
       action | post, put, date_abort
       merge dicts
       response
          encode
          status_code: 200
       exceptions 

"""

@clinicaltrials.command(help="Pipe in, or enter list of names or ids followed by Ctrl-D")
@click.argument('trial-number', nargs=1)
def post_or_put_trial_meta(trial_number):
    _post_or_put_trial_meta(trial_number)

def _post_or_put_trial_meta(trial_number):
    trialCsvText = plugins.clinicaltrialsus.test.getSingleTrialAsCsvText(trial_number)
    csvTrialDict =  plugins.clinicaltrialsus.test.makeDictFromTrialCsvText(trialCsvText)
    plugin = Plugin()
    getUrl = gsrs.config.get_base_url() + 'clinicaltrialsus/' + trial_number
    args = {}
    getResponse = gsrs.ezrest.get(getUrl, trial_number, **args)
    if(getResponse.status_code and getResponse.status_code == 200):
        gsrsTrialDict = json.loads(getResponse.text)
        gsrsTrialDict.update(csvTrialDict)
        putUrl = gsrs.config.get_base_url() + 'clinicaltrialsus'
        args = {}
        putResponse = gsrs.ezrest.put(putUrl, trial_number, json.dumps(gsrsTrialDict, indent=2), **args)
    else: 
        postUrl = gsrs.config.get_base_url() + 'clinicaltrialsus'
        args = {}
        response = gsrs.ezrest.post(postUrl, trial_number, json.dumps(csvTrialDict, indent=2), **args)
 

@clinicaltrials.command(help="Download csv file from clinicaltrials.gov")
# @click.argument('csv_file', nargs=1)
def download_csv_file():
    plugins.clinicaltrialsus.test.bulkDownloadTrialsByPage()

@clinicaltrials.command(help="Download csv file from clinicaltrials.gov")
# @click.argument('csv_file', nargs=1)
def extract_ids_from_csv_file():
    plugins.clinicaltrialsus.test.extractIdsFromCsvFile()

@clinicaltrials.command(help="Update meta data on gsrs instance, using a source csv file")
@click.argument('csv_file', nargs=1)
def bulk_post_or_put_trial_meta(csv_file):
    csv_file = 'eggs.csv'
    with open(csv_file, mode='r') as file:
        plugin = Plugin()
        csv_reader = csv.DictReader(file)
        trials = []
        for row in csv_reader:
            trials.append(row)
        sortedTrials = sorted(trials, key=lambda d: d['NCT Number'])
        for csvTrialDict in sortedTrials:
            logList = []
            trial_number = csvTrialDict['NCT Number']
            logList.append(trial_number)
            getUrl = gsrs.config.get_base_url() + 'clinicaltrialsus/' + trial_number
            args = {}
            logList.append('GET')
            getResponse = gsrs.ezrest.get(getUrl, trial_number, **args)
            if getResponse.status_code: 
                logList.append(str(getResponse.status_code))
            else:
                logList.append('')
            if(getResponse.status_code and getResponse.status_code == 200):
                logList.append('PUT')
                gsrsTrialDict = json.loads(getResponse.text)
                gsrsTrialDict.update(csvTrialDict)
                putUrl = gsrs.config.get_base_url() + 'clinicaltrialsus'
                args = {}
                putResponse = gsrs.ezrest.put(putUrl, trial_number, json.dumps(gsrsTrialDict, indent=2), **args)
                if putResponse.status_code: 
                    logList.append(str(putResponse.status_code))
                else:
                    logList.append('')
                if putResponse.status_code and not putResponse.ok  and putResponse.text: 
                    logList.append(putResponse.text)
                else:
                    logList.append('')
            else: 
                logList.append('POST')
                postUrl = gsrs.config.get_base_url() + 'clinicaltrialsus'
                args = {}
                gsrsTrialDict = plugins.clinicaltrialsus.test.makeGsrsTrialDictFromCsvDict(csvTrialDict)
                postResponse = gsrs.ezrest.post(postUrl, trial_number, json.dumps(gsrsTrialDict, indent=2), **args)
                if postResponse.status_code: 
                    logList.append(str(postResponse.status_code))
                else:
                    logList.append('')
                if postResponse.status_code and not postResponse.ok and postResponse.text: 
                    logList.append(postResponse.text)
                else:
                    logList.append('')
            logList.append("\n")
            gsrs.logging.logSummary("\t".join(logList))
    
if __name__ == 'plugins.clinicaltrials':
    pass




