from setuptools import setup

setup(
    # Module data
    name = 'esalib',
    version = '1.1.0',
    description = 'Utilities for the ESA use cases, as SSHManager, FileManager and custom Logging',
    # Contact data
    url = 'https://www.cisco.com',
    author = 'Cisco',
    author_email = [
        'dalanisr@cisco.com',
        'rferrert@cisco.com',
        'iroldanl@cisco.com',
    ],
    license = 'MIT',
    packages = ['esalib'],
    zip_safe = False,
    # Dependencies
    install_requires = [
        'paramiko==2.7.2',
        'click==8.0.1'
    ]
)
