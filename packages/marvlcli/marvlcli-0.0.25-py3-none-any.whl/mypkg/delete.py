import os
import subprocess
import click
import marvlcli
import json

@click.group()
def delete():
    pass


@delete.command()
# @click.argument("output_type", type=click.Choice(OUTPUTTYPE), default="table")
@click.argument("name", type= str, required=1)
def vm(name):
    marvlcli.export_openrc()
    output = subprocess.check_output('openstack server delete ' + name , shell=True)
    #url = output.decode().splitlines()[5].split('|')[2].split(' ')[1].replace('https://','wss://')
    print(json.dumps(output.decode("utf-8")))
    #os.system('python3 client.py '+ url)
    # click.echo('This is the zone subcommand of the cloudflare command')
