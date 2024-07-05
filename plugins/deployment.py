"""
"""
import sys
import platform
import shutil
sys.path.append('lib')
sys.path.append('./')
import subprocess
import pathlib
import os
import json
import click
import gsrs.ezrest
import gsrs.config
import gsrs.click
import gsrs.utils
from ppretty import ppretty
from datetime import datetime
import subprocess
import string
import yaml


class Plugin:
    def __init__(self, *args, **kwargs):
        pass

    def deployment(self, list):
        pass

## This is not part of class.

 
def load_deployment_yaml(deployment):
    # First read to get the context
    f = 'config/deployment.'+deployment+'.yaml'
    l1 = yaml.SafeLoader
    with open(f) as file: x1 = yaml.load(file, Loader=l1)
    context = x1['deployments'][deployment]['context']

    # Then, read with interpolation of the context variables
    def string_constructor(loader, node):
        t = string.Template(node.value)
        value = t.substitute(context)
        return value
    l2 = yaml.SafeLoader
    l2.add_constructor('tag:yaml.org,2002:str', string_constructor) 
    token_re = string.Template.pattern
    l2.add_implicit_resolver('tag:yaml.org,2002:str', token_re, None)
    with open(f) as file: x2 = yaml.load(file, Loader=l2)
    del x2['deployments'][deployment]['context']
    return x2

## CLI commands specific to deploymentgroup 

@click.group()
def deploymentgroup():
    pass

@deploymentgroup.group()
def deployment():
    pass

@deployment.command(help="List java processes")
@click.argument('deployment', nargs=1)


def psauxjava(deployment):
    plugin = Plugin()
    deployment_config=load_deployment_yaml(deployment)
    command = 'ps -aux | grep java'
    if (platform.system()=='Darwin'):
       command = 'ps aux | grep java'
    output = subprocess.getoutput(command)
    print(output)

@deployment.command(help="Stop tomcat service")
def stop_tomcat(deployment):
    strategy = deployment_config['deployments'][deployment]['strategy']
    if(strategy=='single_tomcat'):
        single_tomcat_stop_tomcat(deployment)

def single_tomcat_stop_tomcat(deployment): 
    command = deployment_config['deployments'][deployment]['single_tomcat']['stop_tomcat']      
    normal = subprocess.run(command, shell=True)
    if (not normal.stdout == None): 
        print(normal.stdout)

@deployment.command(help="Start tomcat service")
def start_tomcat(deployment):
    strategy = deployment_config['deployments'][deployment]['strategy']
    if(strategy=='single_tomcat'):
        single_tomcat_start_tomcat(deployment)

def single_tomcat_start_tomcat(deployment): 
    command = deployment_config['deployments'][deployment]['single_tomcat']['start_tomcat']      
    normal = subprocess.run(command, shell=True)
    if (not normal.stdout == None): 
        print(normal.stdout)

@deployment.command(help="Restart tomcat service")
def restart_tomcat(deployment):
    strategy = deployment_config['deployments'][deployment]['strategy']
    if(strategy=='single_tomcat'):
        single_tomcat_restart_tomcat(deployment)

def single_tomcat_restart_tomcat(deployment): 
    command = deployment_config['deployments'][deployment]['single_tomcat']['restart_tomcat']      
    normal = subprocess.run(command, shell=True)
    if (not normal.stdout == None): 
        print(normal.stdout)

@deployment.command(help="Tomcat status")
def restart_tomcat(deployment):
    strategy = deployment_config['deployments'][deployment]['strategy']
    if(strategy=='single_tomcat'):
        single_tomcat_tomcat_status(deployment)

def single_tomcat_tomcat_status(deployment): 
    command = deployment_config['deployments'][deployment]['single_tomcat']['tomcat_status']      
    normal = subprocess.run(command, shell=True)
    if (not normal.stdout == None): 
        print(normal.stdout)

@deployment.command(help="Build frontend distribution")
@click.argument('deployment', nargs=1)
@click.option('--confirm', default=False)
def build_frontend_distribution(deployment, confirm):
    deployment_config = deployment_config=load_deployment_yaml(deployment)
    frontend_repo_dir = deployment_config['deployments'][deployment]['frontend']['repo']['dir']
    frontend_repo_build_dir = pathlib.PurePath(frontend_repo_dir, 'dist/browser')
    build_command =  deployment_config['deployments'][deployment]['frontend']['repo']['builder']
    frontend_service_static_dir =  pathlib.PurePath(services_impl_dir,'frontend/src/main/resources/static')
    if (confirm==False):
        print("The following directories will be removed and rebuilt, run again with --confirm=True to proceed.")
        print("frontend_repo_build_dir: " + str(frontend_repo_build_dir))
    if (confirm==True):
        os.chdir(frontend_repo_dir)
        if (pathlib.Path(frontend_repo_build_dir).exists()):
            shutil.rmtree(frontend_repo_build_dir)
        normal1 = subprocess.run(build_command, shell=True)
        if (not normal1.stdout == None):
            print(normal1.stdout)
    
@deployment.command(help="Copy frontend distribution to service static folder")
@click.argument('deployment', nargs=1)
@click.option('--confirm', default=False)
def copy_frontend_distribution_to_service_static_folder(deployment, confirm):
    deployment_config = deployment_config=load_deployment_yaml(deployment)
    frontend_repo_dir = deployment_config['deployments'][deployment]['frontend']['repo']['dir']
    frontend_repo_build_dir = pathlib.PurePath(frontend_repo_dir, 'dist/browser')
    build_command =  deployment_config['deployments'][deployment]['frontend']['repo']['builder']
    services_impl_dir = deployment_config['deployments'][deployment]['services_impl']['dir']  
    frontend_service_static_dir =  pathlib.PurePath(services_impl_dir,'frontend/src/main/resources/static')
    if (confirm==False):
        print("The following directories will be removed and rebuilt, run again with --confirm=True to proceed.")
        print("frontend_service_static_dir: " + str(frontend_service_static_dir))
    if (confirm==True):
        shutil.rmtree(frontend_service_static_dir)
        shutil.copytree(frontend_repo_build_dir, frontend_service_static_dir)


@deployment.command(help="Run a maven installer on a starter module in a deployment.")
@click.argument('deployment', nargs=1)
@click.option('--name-like', required=True)
@click.option('--run-tests', default=False)
def maven_install_module(deployment, name_like, run_tests=False):
    deployment_config=load_deployment_yaml(deployment)
    plugin = Plugin()
    if(name_like==None):
        print("Value for --name-like option is required.")
        sys.exit() 
    name_like = name_like.strip()

    base_dir = deployment_config['deployments'][deployment]['base_dir']
    starters = deployment_config['deployments'][deployment]['starters']['modules']
    if (not type(starters) is list ): 
        print("A list of modules in the configuration is required.")
        sys.exit() 
    targets = list(filter(lambda k: name_like in k, starters))
    if (targets == None or len(targets)==0):
        print("No modules containing --name-like value were found.") 
    elif (len(targets)>1): 
        print("More than one module contains text provided with name-like. Please refine.") 
    elif (len(targets)==1):
        target = targets[0]
        starter_dir = pathlib.PurePath(base_dir, 'starters', target)
        if(str(starter_dir)==None or (str(starter_dir).strip()=='')): 
            print("The directory provided is an none or empty.")
            sys.exit() 
        maven_command = './mvnw clean -U install -DskipTests'
        if (not run_tests):
            maven_command += ' -DskipTests'
        os.chdir(starter_dir)
        normal = subprocess.run(maven_command, shell=True)
        if (not normal.stdout == None): 
            print(normal.stdout)

@deployment.command(help="Run a maven packager on a service in a deployment.")
@click.argument('deployment', nargs=1)
@click.option('--name-like', required=True)
@click.option('--more-options')
@click.option('--run-tests', default=False)
def maven_package_service_and_deploy(deployment, name_like, more_options, run_tests=False):
    deployment_config=load_deployment_yaml(deployment)
  
    plugin = Plugin()
    if(name_like==None):
        print("Value for --name-like option is required.")
        sys.exit() 
    name_like = name_like.strip()
    services_impl_dir = deployment_config['deployments'][deployment]['services_impl']['dir']
    services = deployment_config['deployments'][deployment]['services_impl']['services']
    if (not type(services) is list ): 
        print("A list of services in the configuration is required.")
        sys.exit() 
    targets = list(filter(lambda k: name_like in k, services))
    if (targets == None or len(targets)==0):
        print("No services containing --name-like value were found.") 
    elif (len(targets)>1): 
        print("More than one service contains text provided with name-like. Please refine.") 
    elif (len(targets)==1):
        target = targets[0]
        target_service_dir = pathlib.PurePath(services_impl_dir, target)
        if(str(target_service_dir)==None or (str(target_service_dir).strip()=='')): 
            print("The directory provided is an none or empty.")
            sys.exit() 
        maven_command = './mvnw clean -U package -DskipTests'
        if (not run_tests):
            maven_command += ' -DskipTests'
        if (more_options!=None):
            maven_command += more_options


        os.chdir(target_service_dir)
        normal = subprocess.run(maven_command, shell=True)
        if (not normal.stdout == None): 
            print(normal.stdout)

def single_tomcat_copy_config(source, target, uid, gid, permissions):
    shutil.copy(source, target)
    ose.fchown(target, uid, gid)
    os.chmod(path, S_IREAD)
    os.chmod(path, stat.S_IRGRP)

def embedded_tomcat_copy_config(source, target):
    shutil.copy(source, target)

@deployment.command(help="Send a file to aws storage []")
@click.argument('storagekey', nargs=1)
@click.argument('sourcefilename', nargs=1, type=click.Path(exists=True))
@click.argument('targetfilename', nargs=1, type=click.Path(), default='.')
def sendfiletostorage(sourcefilename, targetfilename):
    plugin = Plugin()
    targetpath=''
    config_error = false
    try:
        storagedir=deployment_config['storage'][storagekey]['dir']
    except KeyError:
        config_error = True
        print("The storage key or the associate dir values does not exist.")
    if(not config_error):
        if (storagebasepath==None or storagedir==storagebasepath.strip() ==''):
            raise Exception("Configuration missing for 'storage'.")
        if (sourcefilename==None or targetfilename==None):
            print("Arguments for src and dst required; you may use '.' for the 'tarat filename. Ths indicates that the source and target filenames should be the same.")
        else:
            targetpath = "s3://gsrs-storage/"+targetfilename.strip()
            subprocess.run(["echo",  'aws', 's3', 'cp', sourcefilename, targetpath])
        pass
'''


deployment database x y  
create
wipe --name
names
'''




if __name__ == 'plugins.deployment':
    # deploymentgroup()
    pass
