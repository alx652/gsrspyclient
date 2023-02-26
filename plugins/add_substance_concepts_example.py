"""
"""
import sys
sys.path.append('lib')
sys.path.append('./')
import json
import click
import gsrs.ezrest
import gsrs.config
import gsrs.click
import gsrs.utils
import pandas as pandas
import csv

class Plugin:
    # def __init__(self, *args, **kwargs):
    #    print ('Plugin init ("substance_exists"):', args, kwargs)

    def get_concept_template(self):
        return """
        {
          "definitionType": "PRIMARY",
          "definitionLevel": "COMPLETE",
          "substanceClass": "concept",
          "status": "non-approved",
          "uuid":"_SUBSTANCE_UUID_",
          "names": [
            {
              "deprecated": false,
              "name": "_SUBSTANCE_NAME_",
              "type": "cn",
              "preferred": false,
              "displayName": true,
              "references": [
                "_REFERENCE_UUID1_"
              ],
              "access": []
            }
          ],
          "references": [
            {
              "uuid": "_REFERENCE_UUID1_",
              "citation": "_CITATION_",
              "docType": "_DOCTYPE_",
              "publicDomain": true,
              "tags": [
                "PUBLIC_DOMAIN_RELEASE"
              ],
              "access": []
            }
          ],
          "access": [
            "protected"
          ]
        }
        """

# Example data -- Typically a substance would have more than one name and there'd be more than one reference.
# This is a very simple example.
# _SUBSTANCE_UUID_	_SUBSTANCE_NAME_	_REFERENCE_UUID1_	_DOCTYPE_	_CITATION_
# f6391de8-19ad-489c-a6e8-c156fdfbf91b	CONCEPT_NAME1	e7dcc059-7f47-4815-8444-2157381b8f17	WEBSITE	Some Citation 1
# de5303d9-9423-436c-8e53-d17e19226da1	CONCEPT_NAME2	e28d1ea0-3b51-4321-9f3f-2c002ed6a728	WEBSITE	Some Citation 2
# 4c7c4a83-8d2a-4d38-9b8b-cb36b21acc2e	CONCEPT_NAME3	51ee6efa-93c3-42ae-b385-e599aab41052	WEBSITE	Some Citation 3




    def post_concept(self, data):
        # substance_uuid = str(uuid.uuid4())
        # reference_uuid1 = str(uuid.uuid4())
        # json_text = json_text.replace('_SUBSTANCE_UUID_', substance_uuid)
        # json_text = json_text.replace('_REFERENCE_UUID1_', reference_uuid1)
        # json_text = json_text.replace('_SUBSTANCE_NAME_', str(int(time.time())))
        json_text = self.get_concept_template()
        for key in data.keys():
            json_text = json_text.replace(key, data[key])
        # print(json_text)
        url = gsrs.config.get_base_url() + 'substances'
        args = {}
        gsrs.ezrest.post(url, '', json_text, **args)


## This is not part of class.
## CLI commands specific to substances_exist

@click.group()
def add_substance_concepts_example_group():
    pass

@add_substance_concepts_example_group.command(help="Pipe in, or enter list of names or ids followed by Ctrl-D")
# e.g. cat temp.txt | python3 bin/gsrspyclient.py substancesexist
def addsubstanceconcepts():
    plugin = Plugin()
    print("Enter tab delimited data followed by Ctrl-D")
    # lines = sys.stdin.read().splitlines()
    data = pandas.read_csv(sys.stdin, sep='\t', quoting=csv.QUOTE_NONE)
    for record in data.to_dict(orient='records'):
        plugin.post_concept(record)

    # plugin.substances_exist(lines)

# add commands to the main @click menu
gsrs.click.manager.add_source(add_substance_concepts_example_group)
