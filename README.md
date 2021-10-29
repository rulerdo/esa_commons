# esa-commons
Common Libraries for ESA.

## Installation
To install the utils, execute the following command:
```
pip install git+https://wwwin-github.cisco.com/rferrert/esa-commons.git
```

If you need a particular version, install it by the branch name:
```
pip install git+https://wwwin-github.cisco.com/rferrert/esa-commons.git@[version]
```

## Utils
This library provides the following utils ready to be used:
- ESASSHManager: To handle SSH connection to the remote ESA. It supports execution of commands either at Linux shell level or at ESA's CLI level.
- ESAFileManager: To retrieve and send files to the remote ESA. It also provides methods to analyze and search for patterns in local files, it comes with a practical facade to get all the essential files from ESA and even search for values in them (mainly in the log file).
- ESAStateManager: To keep track of ESA's parameters such as serial and version numbers and tenant ID. The values are retrieved from the files obtained via the ESAFileManager.
- ESAParameters: To get the required parameters for the use cases via CLI arguments. It also initializes the application Logger.
- EmailManager: To send emails in an easy way. It supports attachments and has a very intuitive building process.

## Test
To test the utils, execute the following command:
```
python -m unittest discover -v
```
