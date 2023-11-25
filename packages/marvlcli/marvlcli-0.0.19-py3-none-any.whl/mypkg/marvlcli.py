import click
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

@click.group
def mycommands():
    pass


# def load_resources():
#     f =  open("./resources.yaml", "r")
#     return yaml.safe_load(f)

# def load_commands():
#     f =  open("./commands.yaml", "r")
#     return yaml.safe_load(f)

def load_payloads():
    f =  open("payloads.yaml", "r")
    return yaml.safe_load(f)
def load_user():
    f = open("user.json", "r")
    return json.loads(f.read())

def load_cred():
    f = open("cred.json", "r")
    return json.loads(f.read())
        
def export_openrc():
    user = load_user()
    os.environ['OS_AUTH_URL']='https://marvlbyte.com:5000/v3/'
    os.environ['OS_PROJECT_DOMAIN_NAME']='users'
    os.environ['OS_REGION_NAME']='RegionOne'
    os.environ['OS_APPLICATION_CREDENTIAL_ID']=load_cred()['id']
    os.environ['OS_APPLICATION_CREDENTIAL_SECRET']=load_cred()['secret']
    os.environ['OS_INTERFACE']='public'
    os.environ['OS_IDENTITY_API_VERSION']='3'
    os.environ['OS_AUTH_TYPE']='v3applicationcredential'
    os.environ['OS_USER_ID']=load_user()['id']
    # os.system('echo $OS_PROJECT_ID')
    #print(os.system('openstack server list'))
    
def deleteAppCredential(cred_id):
    export_openrc()
    os.system('openstack application credential delete '+ cred_id)
    
    

@click.command
@click.option("-t", "--token", type=str, prompt="Enter your token id from marvlbyte cloud console", help="The token id is available at the top right corner dropdown menu on https://marvlbyte.com/base/overview page", required=1)
@click.option("-u", "--user_id", type=str, prompt="Enter your userId from marvlbyte cloud console", help="The userId is available at the top right corner dropdown menu on https://marvlbyte.com/base/overview page", required=1)
def init(token, user_id):
    if os.path.isfile("user.json") is False:
        cred_data = load_payloads()['app_credential']
        user_url = "https://marvlbyte.com:5000/v3/users/"+user_id
        headers = {'access-control-allow-origin': "*", "X-Auth-Token": token, "Accept": "*/*", "Content-Type": "application/json"}
        user_resp=requests.get(user_url,headers=headers)
        click.echo(user_resp.content)
        user = json.loads(user_resp.content)["user"]
        user_id = user['id']
        user_name = user['name']
        domain_id = user['domain_id']
        click.echo(cred_data)
        cred_url ="https://marvlbyte.com:5000/v3/users/"+user_id+"/application_credentials"
        cred_resp = requests.post(cred_url, cred_data, headers=headers)
        cred = json.loads(cred_resp.content)['application_credential']
        with open(os.path.abspath("user.json"), "w") as f:
            f.write(json.dumps(cred))
        with open(os.path.abspath("user.json"), "w") as f:
            f.write(json.dumps(user))
        click.echo(f"You are now logged in!")
    else:

        print("\n\n\t\tYou are already logged in with email id " + load_user()['email']+". \n\n\n\tUsage:\t\t marvl logout \t\t to logout\n")    


@click.command
def logout():
    if os.path.isfile("user.json") is True:
        os.remove(os.path.abspath("cred.json"))
        os.remove(os.path.abspath("user.json"))
        cred = load_cred()
        deleteAppCredential(cred["id"])
        print("logged out!!")
    else:
        print("\n\n\t\t You are not logged in yet! \n\n\n\tUsage:\t\t marvl init \t\t to login\n")
    
 
 
 
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
    click.echo("\n\tFor documentations on marvlbyte visit https://docs.marvlbyte.com and search any topic\n\n\n\t\t\tFor dashboard, please visit\n\n\t\t\t https://marvlbyte.com\n\n\n For more information on our affiliate program visit our affiliate program page at https://marvlbyte.com/pages/affiliate\n\n\n")
    mycommands()
