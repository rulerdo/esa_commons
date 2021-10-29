from setuptools import setup


setup(
    # Module data
    name = 'esa_commons',
    version = '0.1.1',
    description = 'Utilities for the ESA use cases, as SSHManager, FileManager and custom Logging',
    # Contact data
    url = 'https://www.cisco.com',
    author = 'Cisco',
    author_email = [
        'dalanisr@cisco.com',
        'rferrert@cisco.com'
    ],
    license = 'MIT',
    packages = [
        'utils',
        'esa_utils',
        'infrastructure'
    ],
    zip_safe = False,
    # Dependencies
    install_requires = [
        'paramiko==2.7.2',
        'click=8.0.1'
    ]
)
