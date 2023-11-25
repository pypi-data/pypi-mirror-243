import os
import click
import marvlcli
import subprocess

@click.group()
def ssh():
    pass


# @ssh.command()
# def create():
#     click.echo('This is the zone subcommand of the cloudflare command')


@ssh.command()
@click.argument("name", type= str, required=1)
def vm(name):
    marvlcli.export_openrc()
    output = subprocess.check_output('openstack console url show --serial ' + name, shell=True)
    print(output)
    url = output.decode().splitlines()[5].split('|')[2].split(' ')[1].replace('https://','wss://').replace('6080', '6080').replace('/vnc_lite.html?path=%3Ftoken%3D', '/?token=')
    print(url)
    os.system('python3 client.py '+ url)
    # click.echo('This is the zone subcommand of the cloudflare command')
