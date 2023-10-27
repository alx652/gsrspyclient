"""
Plugin allows for bulk add or disactivating of GSRS users.
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
import pandas
import csv
import pdb
# Later put these values in default config and optionally a config for eaach instance.

basicRoles = tuple('Query'.split())
intermediateRoles = tuple('Query DataEntry Updater'.split())
advancedRoles = tuple('Query DataEntry SuperDataEntry Updater SuperUpdate Approver'.split())
adminRoles = tuple('Query DataEntry SuperDataEntry Updater SuperUpdate Approver Admin'.split())

basicGroups = tuple()
intermediateGroups = tuple()
advancedGroups = tuple()
adminGroups = tuple('admin'.split())

rolesRecipes = {}
rolesRecipes['basic'] = basicRoles
rolesRecipes['intermediate'] = intermediateRoles
rolesRecipes['advanced'] = advancedRoles
rolesRecipes['admin'] = adminRoles

groupsRecipes = {}
groupsRecipes['basic'] = basicGroups
groupsRecipes['intermediate'] = intermediateGroups
groupsRecipes['advanced'] = advancedGroups
groupsRecipes['admin'] = adminGroups

class Plugin:
    def __init__(self, *args, **kwargs):
        pass

    def users(self, list):
        pass


## The below is NOT part of class.
## CLI functions/commands specific to users_group

@click.group()
def usersgroup():
    pass

@usersgroup.group()
def users():
    pass

@users.command(help="Pipe in, or enter headers followed by select user profiles attributes. Finally type Ctrl-D.")
# @click.option('-r', '--roles-recipe', 'string')
def create(**kwargs):
    """
    CREATE:

    Make a TSV file with the following headers and data underneath:
        username
        email
        password
        rolesRecipe (optional)
        groupsRecipe (optional)

    Both rolesRecipe and groupsRecipe should be one of:
        basic
        intermediate
        advanced
        admin
        (basic is the default, see code for associated roles and groups)

    Run like so:
        cat work/newusers.tsv | python3 bin/gsrspyclient.py users create

    """
    plugin = Plugin()
    # Expecting TSV format
    data = pandas.read_csv(sys.stdin, sep='\t', quoting=csv.QUOTE_NONE)
    for record in data.to_dict(orient='records'):
        groups = []
        userProfile = json.loads('{"username":"","isActive":true,"email":"","roles":["Query","DataEntry"],"groups":[],"password":""}')
        userProfile['username'] = record['username']
        userProfile['password'] = record['password']
        userProfile['email'] = record['email']
        rr = record['rolesRecipe'] if 'rolesRecipe' in record  else 'basic'
        gr = record['groupsRecipe'] if 'groupsRecipe' in record  else 'basic'
        # print("rolesRecipe:" +  rr + " groupsRecipe:" + gr)
        if (rr and rr in rolesRecipes):#
            userProfile['roles'] = rolesRecipes[rr]
        else:
            userProfile['roles'] = rolesRecipes['basic']
        if (gr and gr in groupsRecipes):
            userProfile['groups'] = groupsRecipes[gr]
        else:
            userProfile['groups'] = groupsRecipes['basic']
        # print(json.dumps(userProfile))
        url = gsrs.config.get_base_url() + 'users'
        args = {}
        response = gsrs.ezrest.post(url, userProfile['username'], json.dumps(userProfile), **args)
        # print(userProfile['username'] + ':' + response.status_code)
        # print(response)

@users.command(help="Pipe in, or enter 'username' on first line followed by a list of usernames one per line. Finally type Ctrl-D.")
def deactivate(**kwargs):
    """
    Make a TSV file with the following headers and data underneath:
        username

    Run like so:
        cat deactivates.tsv | python3 bin/gsrspyclient.py users deactivate
    """
    plugin = Plugin()
    # Expecting TSV format
    data = pandas.read_csv(sys.stdin, sep='\t', quoting=csv.QUOTE_NONE)
    for record in data.to_dict(orient='records'):
        username = record['username']
        print(username)
        url = gsrs.config.get_base_url() + 'users/' + username
        args = {}
        response = gsrs.ezrest.delete(url, username, '{}', **args)

if __name__ == 'plugins.users':
    # usersgroup()
    pass
    
if __name__ == '__main__':
    # add commands to the main @click menu
    # gsrs.click.manager.add_source(usersgroup)
    pass
