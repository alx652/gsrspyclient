import os
import sys
sys.path.append('lib')
sys.path.append('./')
import json
import click
import csv
import jmespath

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
    trialDict =  plugins.clinicaltrialsus.test.makeGsrsDictFromTrialCsvText(trialCsvText)
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

@clinicaltrials.command(help="Post or put a single trial's meta data source from ct.gov api call.")
@click.argument('trial-number', nargs=1)
@click.option('--skip-if-last-updated-equal', is_flag=True)
def post_or_put_trial_meta(trial_number, skip_if_last_updated_equal):
    newMetaCsvText = plugins.clinicaltrialsus.test.getSingleTrialAsCsvText(trial_number)
    newMetaCsvDict =  plugins.clinicaltrialsus.test.makeCsvDictFromTrialCsvText(newMetaCsvText)
    _post_or_put_trial_meta(newMetaCsvDict, skip_if_last_updated_equal)

def _post_or_put_trial_meta(newMetaCsvDict, skip_if_last_updated_equal):
    logList = []
    trial_number = newMetaCsvDict['NCT Number']
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
        gsrsTrialDict = json.loads(getResponse.text)
        if skip_if_last_updated_equal and plugins.clinicaltrialsus.test.skipPutWhenLastUpdateDatesEqual(gsrsTrialDict['lastUpdated'], newMetaCsvDict['Last Update Posted']): 
            logList.append('PUT-SKIPPED')
        else:                            
            logList.append('PUT')
            newMetaAsGsrsDict = plugins.clinicaltrialsus.test.makeGsrsTrialDictFromCsvDict(newMetaCsvDict)
            gsrsTrialDict.update(newMetaAsGsrsDict)
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
        gsrsTrialDict = plugins.clinicaltrialsus.test.makeGsrsTrialDictFromCsvDict(newMetaCsvDict)
        postResponse = gsrs.ezrest.post(postUrl, trial_number, json.dumps(gsrsTrialDict, indent=2), **args)
        if postResponse.status_code: 
            logList.append(str(postResponse.status_code))
        else:
            logList.append('')
        if postResponse.status_code and not postResponse.ok and postResponse.text: 
            logList.append(postResponse.text)
        else:
            logList.append('')
    gsrs.logging.logAdhoc("\t".join(logList))



@clinicaltrials.command(help="Download csv file from clinicaltrials.gov")
@click.argument('csv_file', nargs=1)
def download_csv_file(csv_file):
    plugins.clinicaltrialsus.test.bulkDownloadTrialsByPage(csv_file)

@clinicaltrials.command(help="Download csv file from clinicaltrials.gov")
@click.argument('csv_file', nargs=1)
def extract_ids_from_csv_file(csv_file):
    plugins.clinicaltrialsus.test.extractIdsFromCsvFile(csv_file)

@clinicaltrials.command(help="Update meta data on gsrs instance, using a source csv file")
@click.argument('csv_file', nargs=1)
@click.option('--skip-if-last-updated-equal', is_flag=True)
def bulk_post_or_put_trial_meta(csv_file, skip_if_last_updated_equal):
    with open(csv_file, mode='r', encoding="utf-8") as file:
        plugin = Plugin()
        csv_reader = csv.DictReader(file)
        trials = []
        for row in csv_reader:
            trials.append(row)
        sortedTrials = sorted(trials, key=lambda d: d['NCT Number'])
        for newMetaCsvDict in sortedTrials:
            _post_or_put_trial_meta(newMetaCsvDict, skip_if_last_updated_equal)


@clinicaltrials.command(help="Pipe in, or enter list of trial ids followed by Ctrl-D")
def delete_trials():
    plugin = Plugin()
    lines = sys.stdin.read().splitlines()
    gsrs.utils.strip_list(lines)
    _delete_trials(lines)

def _delete_trials(ids):
    urlTemplate = gsrs.config.get_base_url() + 'clinicaltrialsus/{0}'
    args = {}
    for id in ids:
        response = gsrs.ezrest.delete(urlTemplate.format(id), id, '', **args)


@clinicaltrials.command(help="Pipe in, or enter list of trial ids followed by Ctrl-D")
@click.option('--show-formatted', is_flag=True)
def get_last_updated_by_trial(show_formatted):
    plugin = Plugin()
    lines = sys.stdin.read().splitlines()
    gsrs.utils.strip_list(lines)
    _get_last_updated_by_trial(lines, show_formatted)

def _get_last_updated_by_trial(ids, show_formatted):
    urlTemplate = gsrs.config.get_base_url() + 'clinicaltrialsus/{0}'
    args = {}
    for id in ids:
        row=[]
        response = gsrs.ezrest.get(urlTemplate.format(id), id, **args)
        dict = json.loads(response.text)
        row.append(str(id))
        row.append(str(dict['lastUpdated']))
        if show_formatted: 
            row.append(datetime.fromtimestamp(dict['lastUpdated']/1000.0).strftime("%Y %m %d %H:%M:%S"))
        print ("\t".join(row))

if __name__ == 'plugins.clinicaltrials':
    pass




