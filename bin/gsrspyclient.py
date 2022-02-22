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
import gsrs.click
import gsrs.logging

if __name__ == '__main__':
    gsrs.click.manager = click.CommandCollection(help=None, no_args_is_help=False)

# For nice intro to plugins see here:
# https://www.youtube.com/watch?v=cbot48lckOs
# Eventually read all plugins from plugins folder and loop through
# loading any registered in config.
plugins = {}
plugins['substances_exist'] = importlib.import_module('plugins.substances_exist')

plugins['add_substance_concepts_example'] = importlib.import_module('plugins.add_substance_concepts_example')

@click.group()
def cli1():
    """
    Demo GSRS Command line interface
    """
    pass

# python> python3 test2.py  cmd1 --context clinicaltrialsus
# @cli1.command()
# @click.option('-c', '--context', required=True)
# @click.option('-h', '--host-key')
# @click.option('-m', '--method')
# @click.option('--id')
# @click.option('--ids-filter-file')
# @click.option('--json-write-folder')
# @click.option('--json-read-folder')
# @click.option('-t', '--id')
# def cmd1(host_key, method, context, id):
#     host_key = gsrs.config.check_host_key(host_key)
#     gsrs.logging.logging.info("The host key is: " + host_key)
#     if host_key is None:
#         raise Exception('Please use the --host-key option or set  default_host_key in the configuration')
#     url_format = gsrs.config.config['host_keys'][host_key]['baseUrl'] + context + '/{}'
#     args = {}
#     click.echo("URL " + url_format.format(id))
#     try:
#       response = gsrs.ezrest.get(url_format.format(id), id, **args)
#       if response:
#          print(response.content)
#     except Exception as e:
#          gsrs.logging.logging.info(e)


@click.group()
def cli2():
    pass


if __name__ == '__main__':
    gsrs.click.manager.add_source(cli1)
    gsrs.click.manager.add_source(cli2)
    gsrs.click.manager()
