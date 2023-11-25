from setuptools import find_packages, setup

setup(
    name="marvlcli",
    version='0.0.19',
    py_modules= ['marvlcli','info','ssh','list', 'create', 'delete', 'client'],
    packages=['package_data'],
    install_requires=[
        'click',
        'pyyaml',
        'python-novaclient',
        'python-cinderclient',
        'python-neutronclient',
        'python-openstackclient',
        'ws4py'
        
    ],
    include_package_data=True,
    package_data={'package_data': ['payloads.yaml', 'myuserdata_marv_default.txt']},
    entry_points='''
    [console_scripts]
    marvl=marvlcli:marvlcli
    
    
    '''
    
)

