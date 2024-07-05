from collections import OrderedDict

class Mapper:
    fieldMap = OrderedDict()
    sourceFields = []

    def __init__(self):
        fieldMapBlock = '''
sourceName	gsrsName	type	length	makerFunction 
NCT Number	trialNumber	string	255	
Study Title	title	string		
Study URL	url	string	2000	
Acronym	acronym	string		
Study Status	status	string	500	
Brief Summary		string		
Study Results	studyResults	string		
Conditions	conditions	string		
Interventions	intervention	string		
Primary Outcome Measures	outcomeMeasures	string		
Secondary Outcome Measures		string		
Other Outcome Measures		string		
Sponsor	sponsor	string		
Collaborators		string		
Sex	gender	string		
Age	ageGroups	string		
Phases	phases	string		
Enrollment	enrollment	string		
Funder Type	fundedBys	string		
Study Type	studyTypes	string		
Study Design	studyDesigns	string		
Other IDs	otherIds	string		
Start Date	startDate	date		makeDate
Primary Completion Date	primaryCompletionDate	date		makeDate
Completion Date	completionDate	date		makeDate
First Posted	firstReceived	date		makeDate
Results First Posted	resultsFirstReceived	date		makeDate
Last Update Posted	lastUpdated	date		makeDate
Locations	locations	string		
Study Documents		string		
'''
        # __init__ cont'd
        lines = fieldMapBlock.split("\n"); 
        c = 0
        for l in lines:
            l=l.strip()
            if l=='':
                continue
            if c == 0:
                self.sourceFields = l.split("\t")
                c = c+1 
                continue
            c = c+1  
            values = l.split("\t")
            for i in range(len(values), len(self.sourceFields)): 
                values.append('')
            d = dict(zip(self.sourceFields, values))
            self.fieldMap[d['sourceName']]=d
