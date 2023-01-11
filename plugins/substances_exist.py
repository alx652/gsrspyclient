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

class Plugin:
    # def __init__(self, *args, **kwargs):
    #    print ('Plugin init ("substance_exists"):', args, kwargs)

    def substances_exist(self, list):
        url = gsrs.config.get_base_url() + 'substances/@exists'
        args = {}

        response = gsrs.ezrest.post(url, '', json.dumps(list), **args)
        results = json.loads(response.content)
        for item in list:
            if item in results['found']:
                print("\t".join([results['found'][item]['query'], results['found'][item]['id'],results['found'][item]['url']]))
            else:
                print("\t".join([item, "", ""]))




## This is not part of class.
## CLI commands specific to substances_exist_group

@click.group()
def substances_exist_group():
    pass

@substances_exist_group.command(help="Pipe in; or enter list of names or ids followed by Ctrl-D")
# e.g. cat temp.txt | python3 bin/gsrspyclient.py substancesexist
def substancesexist():
    plugin = Plugin()
    print("\nEnter a list of substance uuids or names one per line, followed by Ctrl-D\n")
    lines = sys.stdin.read().splitlines()
    gsrs.utils.strip_list(lines)
    # print(str(lines))
    plugin.substances_exist(lines)

# add commands to the main @click menu
gsrs.click.manager.add_source(substances_exist_group)
