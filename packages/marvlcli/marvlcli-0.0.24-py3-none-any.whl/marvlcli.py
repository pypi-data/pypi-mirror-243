import random
import string
from urllib.error import URLError
import click
import pkg_resources
import yaml
import sys
import json
import requests
import os
import subprocess
from info import info
from ssh import ssh
from list import list
from create import create
from delete import delete
import urllib.request



@click.group
def mycommands():
    pass


def load_user():
    if os.path.isfile(pkg_resources.resource_filename(__name__, 'package_data/user.json')) is True:

        file_name_with_path = pkg_resources.resource_filename(__name__, 'package_data/user.json')
        f = open(file_name_with_path, "r")
        return json.loads(f.read())
    else:
        click.echo("You are not logged in! Please login with marvl init" )

def load_cred():
    if os.path.isfile(pkg_resources.resource_filename(__name__, 'package_data/cred.json')) is True:
        file_name_with_path = pkg_resources.resource_filename(__name__, 'package_data/cred.json')
        f = open(file_name_with_path, "r")
        return json.loads(f.read())
    else:
        click.echo("You are not logged in! Please login with marvl init" )

        
        
def export_openrc():
    user = load_user()
    if user != None:
        
        os.environ['OS_AUTH_URL']='https://marvlbyte.com:5000/v3/'
        os.environ['OS_PROJECT_DOMAIN_NAME']='users'
        os.environ['OS_REGION_NAME']='RegionOne'
        os.environ['OS_APPLICATION_CREDENTIAL_ID']=load_cred()['id']
        os.environ['OS_APPLICATION_CREDENTIAL_SECRET']=load_cred()['secret']
        os.environ['OS_INTERFACE']='public'
        os.environ['OS_IDENTITY_API_VERSION']='3'
        os.environ['OS_AUTH_TYPE']='v3applicationcredential'
        os.environ['OS_USER_ID']=load_user()['id']
        return True
    else:
        return False
    # os.system('echo $OS_PROJECT_ID')
    #print(os.system('openstack server list'))
    
def deleteAppCredential(cred_id):
    isExported = export_openrc()
    if isExported == True:
        os.system('openstack application credential delete '+ cred_id)
    
    
def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)
    return result_str

def app_cred_payload():
    s = '''{
      "application_credential": {
        "name": "unrestricted_access_created_by_marvcli2",
        "description": "Application credential created by marvcli.",
        "unrestricted": true
      }
    }'''
    return yaml.safe_load(s)

def check(name):

    import urllib.request
    from pip._internal.operations.freeze import freeze

    current_version = ''
    for requirement in freeze(local_only=False):
        pkg = requirement.split('==')
        if pkg[0] == name:
            current_version = pkg[1]
    try:
        contents = urllib.request.urlopen('https://pypi.org/pypi/'+name+'/json').read()
        data = json.loads(contents)
        latest_version = data['info']['version']

        if current_version==latest_version:
            click.echo('Latest version (' + click.style(current_version, fg="cyan") + ') of '+str(name)+' is installed')
            return True
        else:
            click.echo(click.style('Version ' + current_version + ' of '+str(name)+' not the latest '+latest_version, fg='yellow'))
            return False
    except requests.HTTPError as e:
        # do something
        click.echo(click.style("Error", fg='red')+": Error code: "+e.code)
    except URLError as e:
    # do something
        click.echo(click.style("Error", fg='red')+": Reason: "+ e.reason)
    else:
        print("latest version could not be checked")
        
        
    

@click.command
@click.option("-t", "--token", type=str, prompt="Enter your token id from marvlbyte cloud console", help="The token id is available at the top right corner dropdown menu on https://marvlbyte.com/base/overview page", required=1)
@click.option("-u", "--user_id", type=str, prompt="Enter your userId from marvlbyte cloud console", help="The userId is available at the top right corner dropdown menu on https://marvlbyte.com/base/overview page", required=1)
def init(token, user_id):
    if os.path.isfile(pkg_resources.resource_filename(__name__, 'package_data/user.json')) is False:

        cred_data = '''{
  "application_credential": {
    "name": "'''+get_random_string(8)+user_id+'''",
    "description": "Application credential created by marvcli.",
    "unrestricted": true
  }
}'''

        user_url = "https://marvlbyte.com:5000/v3/users/"+user_id
        headers = {'access-control-allow-origin': "*", "X-Auth-Token": token, "Accept": "*/*", "Content-Type": "application/json"}
        user_resp=requests.get(user_url,headers=headers)
        click.echo(user_resp.content)
        user = json.loads(user_resp.content)["user"]
        user_id = user['id']
        user_name = user['name']
        domain_id = user['domain_id']
      
        cred_url ="https://marvlbyte.com:5000/v3/users/"+user_id+"/application_credentials"
        cred_resp = requests.post(cred_url, cred_data, headers=headers)

        
        with open(pkg_resources.resource_filename(__name__, 'package_data/user.json'), "w") as f:
            f.write(json.dumps(user))
        cred = json.loads(cred_resp.content)["application_credential"]
        with open(pkg_resources.resource_filename(__name__, 'package_data/cred.json'), "w") as f:
            f.write(json.dumps(cred))
        click.echo(click.style("You are now logged in", fg="cyan"))
    else:

        print("\n\n\t\tYou are already logged in with email id " + load_user()['email']+". \n\n\n\tUsage:\t\t marvl logout \t\t to logout\n")    


@click.command
def logout():
    if os.path.isfile(pkg_resources.resource_filename(__name__, 'package_data/cred.json')) is True:
        cred = load_cred()
        deleteAppCredential(cred["id"])
        os.remove(pkg_resources.resource_filename(__name__, 'package_data/cred.json'))
        
    if os.path.isfile(pkg_resources.resource_filename(__name__, 'package_data/user.json')) is True:
        os.remove(pkg_resources.resource_filename(__name__, 'package_data/user.json'))
    
        
    else:
        print("\n\n\t\t You are not logged in yet! \n\n\n\tUsage:\t\t marvl init \t\t to login\n")
    print("logged out!!")
 
 
 
 ###########################################################################################################################   
# @click.command
# @click.option("--name", prompt="Enter your name", help="The name of the user" )
# def hello(name):
#     click.echo(sys.argv)
#     # click.echo(load_resources())


# PRIORITIES={
#     "o": "Optional",
#     "m": "Medium",
#     "l": "Low",
#     "h": "High",
#     "c": "Crucial"
# }


# @click.command()
# @click.argument("priority", type=click.Choice(PRIORITIES.keys()), default="m")
# @click.argument("todofile", type=click.Path(exists=False), required=0)
# @click.option("-n", "--name", prompt="Enter the todo name", help="name of the to do item")
# @click.option("-d","--desc", prompt="Enter a description", help="The description of the to do item")
# def add_todo(name, desc, priority, todofile):
#     filename= todofile if todofile is not None else "mytodos.txt"
#     with open(filename, "a+") as f:
#         f.write(f"{name}: {desc} [Priority: {PRIORITIES[priority]}]\n")
        

# @click.command()
# @click.argument("idx",  type=int, required=1)
# def delete_todo(idx):
#     with open("mytodos.txt", "r") as f:
#         todo_list = f.read().splitlines()
#         todo_list.pop(idx)
#     with open("mytodos.txt", "w") as f:
#         f.write("\n".join(todo_list))
#         f.write('\n')
        
# @click.command()
# @click.option("-p","--priority", type=click.Choice(PRIORITIES.keys()))
# @click.argument("todofile", type= click.Path(exists=True), required=0)
# def list_todos(priority, todofile):
#     filename = todofile if todofile is not None else "mytodos.txt"
#     with open(filename, "r") as f:
#         todo_list = f.read().splitlines()
#     if priority is None:
#         for idx, todo in enumerate(todo_list):
#             print(f"({idx})-{todo}")
#     else:
#         for idx, todo in enumerate(todo_list):
#             if f"[Priority: {PRIORITIES[priority]}]" in todo:
#                 print(f"({idx})-{todo}")
    
###################################################################################################################################    
mycommands.add_command(ssh)
# mycommands.add_command(hello)
mycommands.add_command(init)  
mycommands.add_command(logout)
mycommands.add_command(list)
mycommands.add_command(create)
mycommands.add_command(info)
mycommands.add_command(delete)



    

    
if __name__=="marvlcli":
    click.echo("\n\tFor documentations on marvlbyte visit "+ click.style("https://docs.marvlbyte.com", fg="cyan")+" and search any topic\n\t\t\tFor dashboard, please visit\n\t\t\t  "+ click.style("https://marvlbyte.com", fg="cyan")+" \n For more information on our affiliate program visit our affiliate program page at  "+ click.style("https://marvlbyte.com/pages/affiliate", fg="cyan")+"\n")
    if check(__name__)==False:
        click.echo(click.style("Warn", fg="yellow") + ":Please update the cli now with the command "+ click.style("pip install marvlcli==<latest_version>", fg='magenta')+" to avoid this warning!\n")
        
    mycommands()
    
    
        
    
        

