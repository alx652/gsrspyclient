
import csv
import mapper
import json


filename = "temp.txt"

fm = mapper.Mapper().fieldMap

fields = []
rows = []

with open(filename, mode='r', encoding="utf-8") as file:
    csv_reader = csv.DictReader(file)
    trials = []
    for row in csv_reader:
        trials.append(row)
    sortedTrials = sorted(trials, key=lambda d: d['NCT Number'])
    for trial in sortedTrials:
        jsonDict = dict()
        for key in fm.keys():
            if 'gsrsName' in fm[key] and fm[key]['gsrsName'] is not None and fm[key]['gsrsName'].strip() != '': 
                jsonDict[fm[key]['gsrsName']] = trial[key]
        print (trial['NCT Number'], "\t", json.dumps(jsonDict)) 


