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
import pandas;
import csv;

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
    # def __init__(self, *args, **kwargs):
    #    print ('Plugin init ("users_add_administrator"):', args, kwargs)

    def users(self, list):
        url = gsrs.config.get_base_url() + 'users'
        args = {}

# END CLASS


## The below is NOT part of class.
## CLI functions/commands specific to users_group

@click.group()
def usersgroup(**kwargs):
    pass;

@usersgroup.group()
def users(**kwargs):
    pass;

@users.command(help="Pipe in; or enter list of user profiles to create or ids followed by Ctrl-D")
# @click.option('-r', '--roles-recipe', 'string')
def create(**kwargs):
    """
    Create a TSV file with the following headers and data underneath:
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
        (basic is the default, see code for associate roles and groups)

    Run like so:
        cat temp.tsv | python3 bin/gsrspyclient.py users create

    """
    plugin = Plugin()
    print("\nEnter a list of substance uuids or names one per line, followed by Ctrl-D\n")

    # Expecting TSV format
    data = pandas.read_csv(sys.stdin, sep='\t', quoting=csv.QUOTE_NONE)

    for record in data.to_dict(orient='records'):
        groups = []
        userProfile = json.loads('{"username":"","isActive":true,"email":"","roles":["Query","DataEntry"],"groups":[],"password":""}');
        userProfile['username'] = record['username']
        userProfile['password'] = record['password']
        userProfile['email'] = record['email']
        rr = record['rolesRecipe'] if 'rolesRecipe' in record  else 'basic'
        gr = record['groupsRecipe'] if 'groupsRecipe' in record  else 'basic'
        # print("rolesRecipe:" +  rr + " groupsRecipe:" + gr)
        if (rr and rr in rolesRecipes):
            userProfile['roles'] = rolesRecipes[rr]
        else:
            userProfile['roles'] = rolesRecipes['basic']
        if (gr and gr in groupsRecipes):
            userProfile['groups'] = groupsRecipes[gr];
        else:
            userProfile['groups'] = groupsRecipes['basic'];
        # print(json.dumps(userProfile))
        url = gsrs.config.get_base_url() + 'users'
        args = {}
        response = gsrs.ezrest.post(url, '', json.dumps(userProfile), **args)
        # print(userProfile['username'] + ':' + response.status_code)
        print(response)

@users.command(help="Pipe in; or enter list of user profiles to create or ids followed by Ctrl-D")
def deactivate(**kwargs):
    plugin = Plugin()
    print("\nEnter a list of substance uuids or names one per line, followed by Ctrl-D\n")

    # Expecting TSV format
    data = pandas.read_csv(sys.stdin, sep='\t', quoting=csv.QUOTE_NONE)

    for record in data.to_dict(orient='records'):
        username = record['username']
        url = gsrs.config.get_base_url() + 'users/' + username
        args = {}
        response = gsrs.ezrest.delete(url, username, '{}', **args)
        # print(userProfile['username'] + ':' + response.status_code)
        print("username:" + username)
        print("response:")
        print(response)


if __name__ == 'plugins.users':
    usersgroup()

if __name__ == '__main__':
    # add commands to the main @click menu
    gsrs.click.manager.add_source(users)
