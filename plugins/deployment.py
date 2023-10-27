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
from datetime import datetime
import subprocess


class Plugin:
    def __init__(self, *args, **kwargs):
        pass

    def deployment(self, list):
        pass

## This is not part of class.
## CLI commands specific to deploymentgroup

@click.group()
def deploymentgroup():
    pass

@deploymentgroup.group()
def deployment():
    pass

@deployment.command(help="List java processes")
def psauxjava():
    plugin = Plugin()
    # subprocess.run(["ps", "-aux", ])
    mycmd=subprocess.getoutput('ps -aux | grep java')
    print(mycmd);

@deployment.command(help="Send a file to aws storage []")
@click.argument('storagekey', nargs=1)
@click.argument('sourcefilename', nargs=1, type=click.Path(exists=True))
@click.argument('targetfilename', nargs=1, type=click.Path(), default='.')
def sendfiletostorage(sourcefilename, targetfilename):
    plugin = Plugin()
    targetpath=''
    config_error = false
    try:
        storagedir=gsrs.config.config['storage'][storagekey]['dir']
    except: KeyError
        config_error = true
        print("The storage key or the associate dir values does not exist.")
    if(!config_error):
        if (storagebasepath==None or storagedir=storagebasepath.strip() ==''):
            raise Exception("Configuration missing for 'storage'.")
        if (sourcefilename==None or targetfilename==None):
            print("Arguments for src and dst required; you may use '.' for the 'tarat filename. Ths indicates that the source and target filenames should be the same.")
        else:
            targetpath = "s3://gsrs-storage/"+targetfilename.strip()
            subprocess.run(["echo",  'aws', 's3', 'cp', sourcefilename, targetpath])
        pass

if __name__ == 'plugins.deployment':
    # deploymentgroup()
    pass
