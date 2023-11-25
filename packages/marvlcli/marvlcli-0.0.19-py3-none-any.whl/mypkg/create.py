import os
import subprocess
import click
import marvlcli


@click.group()
def create():
    pass

OUTPUTTYPE=["json","shell","table","value","yaml"]

IMAGELIST=["CentOs-Stream-8", "CentOs-9", "Ubuntu-18.04", "Ubuntu-20.04", "Ubuntu-22.04", "Fedora-38", "Debian-9", "Debian-10", "Arch-Box", "NetBSD-8.2", "OpenBSD-7.2", "NetBSD-9.3", "OpenBSD7.3", "Cirros"]

FLAVOURLIST=["m1.small", "m1.medium", "m1.large", "m1.xlarge"]

@create.command()
@click.option("--userdata", "-ud",  default="myuserdata_marv_default.txt", prompt="Enter the userdata file path(Optional)", help="Path of a file containing the user data like vm password etc. Default password, 'mypasswd' is set using a default userdata file", type=click.Path(exists=False), required=0)
@click.option("--netid", "-n", default="e083abf4-02af-4be3-a5c1-a0ad9f1030ba", prompt="Enter the private network id (Optional)", help="id of the private network. Default value is e083abf4-02af-4be3-a5c1-a0ad9f1030ba ", required=0)
@click.option("--image", "-i", type=click.Choice(IMAGELIST), default="Ubuntu-22.04", prompt="Enter the image name (Optional)", help="Name of the image. Default value is Ubuntu-22.04", required=0)
@click.option("--flavor", "-f", type=click.Choice(FLAVOURLIST), default="m1.medium", prompt="Enter the flavor name (Optional)", help="Name of the flavor. Default value is m1.medium", required=0)
@click.argument("name", type= str, required=1)
def vm(name, flavor, image, userdata, netid):
    filename= userdata if userdata is not None else "./myuserdata_marv_default.txt"
    marvlcli.export_openrc()
    output = subprocess.check_output('openstack server create ' + name + " --image "+ image + " --flavor "+ flavor + " --availability-zone nova "+ "  --user-data "+ filename + " --nic net-id="+ netid, shell=True)
    print("Your vm is created successfully!!!!!")
    if filename=='myuserdata_marv_default.txt':
        print("Your vm is created with default password 'mypasswd'. Please change the password for security purposes.")
    