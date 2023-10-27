import sys
sys.path.append('lib')
sys.path.append('./')
import os

# exit()
import yaml
import click
import requests
import uuid
import time
import importlib
# from warnings import warn

import gsrs.config
import gsrs.ezrest
import gsrs.logging
import gsrs.click
import traceback
from ppretty import ppretty

# For nice intro to plugins see here:
# https://www.youtube.com/watch?v=cbot48lckOs
# Eventually read all plugins from plugins folder and loop through
# loading any registered in config.

gsrs.click.manager = click.CommandCollection(help=None, no_args_is_help=False)

@click.group()
def cli():
    pass

# print(ppretty(gsrs.click.manager))

# plugins = {}
# print("here0")
# plugins['users'] = importlib.import_module('plugins.users')
# print("here2")
# plugins['substanceutils'] = importlib.import_module('plugins.substanceutils')
# print("here1")


plugins = {}
plugins['users'] = importlib.import_module('plugins.users')
plugins['substanceutils'] = importlib.import_module('plugins.substanceutils')
plugins['deployment'] = importlib.import_module('plugins.deployment')


cli.add_command(getattr(plugins['users'], 'users'))
cli.add_command(getattr(plugins['substanceutils'], 'substanceutils'))
cli.add_command(getattr(plugins['deployment'], 'deployment'))



cli()
