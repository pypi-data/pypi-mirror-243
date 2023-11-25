import os
import subprocess
import click
import marvlcli
import json

@click.group()
def list():
    pass

OUTPUTTYPE=["json","shell","table","value","yaml"]


@list.command()
@click.argument("output_type", type=click.Choice(OUTPUTTYPE), default="table")
def vms(output_type):
    marvlcli.export_openrc()
    output = subprocess.check_output('openstack server list ' + ' -f ' + output_type, shell=True)
    #url = output.decode().splitlines()[5].split('|')[2].split(' ')[1].replace('https://','wss://')
    print(json.dumps(output.decode("utf-8")))