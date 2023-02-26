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
from ppretty import ppretty

class Plugin:
    def __init__(self, *args, **kwargs):
        pass

    def substanceutils(self, list):
        pass

## This is not part of class.
## CLI commands specific to substanceutilsgroup

@click.group()
def substanceutilsgroup():
    pass

@substanceutilsgroup.group()
def substanceutils():
    pass

@substanceutils.command(help="Pipe in, or enter list of names or ids followed by Ctrl-D")
def substancesexist():
    plugin = Plugin()
    lines = sys.stdin.read().splitlines()
    gsrs.utils.strip_list(lines)
    url = gsrs.config.get_base_url() + 'substances/@exists'
    args = {}
    response = gsrs.ezrest.post(url, '', json.dumps(lines), **args)
    results = json.loads(response.content)
    for item in lines:
        if item in results['found']:
            print("\t".join([results['found'][item]['query'], results['found'][item]['id'],results['found'][item]['url']]))
        else:
            print("\t".join([item, "", ""]))

if __name__ == 'plugins.substanceutils':
    substanceutilsgroup()

# add commands to the main @click menu
if __name__ == '__main__':
    gsrs.click.manager.add_source(substanceutilsgroup)
