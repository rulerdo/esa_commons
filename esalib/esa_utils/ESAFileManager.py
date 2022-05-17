# ESA utils
from esalib.utils.logger.Logger import Logger
from .ESASSHAgent import ESASSHAgent
# Utils
from ..utils.files.FileManager import FileManager


class ESAFileManager:
    """
    @version 1.2.3

    Class to get files from ESA and retrieve values from them. It is useful to get relevant values for 
    the state. 
    This class eliminates the need to worry about handling files in other classes, by providing a facade 
    to simply retrieve a remote file by its name/path, and anither facade to retrieve values from already
    obtained files via regular expressions.
    The method et_essential_files is a practical wrapper to get all the necessary files to get ESA's basic
    information (serial number and warnings in the logfile).
    """

    # File names
    ESA_LOG_FILE_NAME               = 'qlogd_alert_messages.dat'
    ESA_SNMPD_CONF_FILE_NAME        = 'snmpd.conf'
    __ESA_REFERENCE_FILE_PREFIX     = 'OLD_' 

    # File locations
    ESA_LOG_FILE_PATH = '/data/db/' + ESA_LOG_FILE_NAME
    ESA_SNMPD_CONF_PATH = '/data/release/current/etc/' + ESA_SNMPD_CONF_FILE_NAME


    def __init__(
        self, 
        ssh_agent: ESASSHAgent
    ):
        """
        @param {ESASSHAgent} ssh_agent SSH agent manager.
        """
        self.ssh_agent: ESASSHAgent = ssh_agent
        # Cached relevant values (to void innecessary file reopening)
        self.serial_number = None
        self.version_number = None

    def get_essential_files(self):
        """
        Retrieves the essential ESA files (SNMPD and log files). 
        These files are used in almost all the use cases, because we can found the essential information
        there, like the serial number in SNMPD conf file, as well as the errors displayed in the log file.
        """
        # We remove the residual files from previous executions, if any.
        self.remove_essential_files()
        # We retrieve the files
        self.get_snmpd_file()
        self.get_esa_serial_number()
        self.get_log_file()

    def remove_essential_files(self):
        """
        Method to remove the essential files (snmpd and log files). 
        This method should be called at the end of the use case, even if - for safety reasons - it is
        automatically called in the get_essential_files method.
        """
        self.safely_remove_file(self.ESA_SNMPD_CONF_FILE_NAME)
        self.safely_remove_file(self.ESA_LOG_FILE_NAME)

    def get_snmpd_file(self):
        """
        Retrieves the SNMPD file from ESA. This file is useful to get the serial and version number of the
        ESA, which are important values for the remediation process.
        """
        # We request the file
        self.ssh_agent.get_file_with_scp(self.ESA_SNMPD_CONF_PATH)

    def get_log_file(self):
        """
        Retrieves the log file from ESA. This file is useful for the remediation process, as we'll need to
        look for a warning message indicating a problem with the tenant_id (Invalid Key).
        """
        self.ssh_agent.get_file_with_scp(self.ESA_LOG_FILE_PATH)

    def upload_file(
        self, 
        file_to_upload: str, 
        destination_path: str
    ):
        """
        @param {str} file_to_upload Path of the local file to upload.
        @param {str} destination_path Remote path to install the uploaded file.

        Uploads a file to the ESA via the ESASSHAgent instance.
        """
        self.ssh_agent.upload_file_with_scp(file_to_upload, destination_path)


    def get_value_from_file(
        self, 
        file_name: str,
        key_value_regex: str
    ) -> str:
        """
        @param {str} file_name The file in which we will look for the values.
        @param {str} key_value_regex The regular expression to perform the search.

        Gets a value from a file, in a key-value structure via a regular expression and by using the 
        FileManager util. 
        To get a value, we can use the regex pattern (.*?) after the key.

        @returns Desired value in file.
        """
        file_manager = FileManager(file_name)
        return file_manager.search_value_with_regex(key_value_regex)

    def is_string_present_in_file(
        self,
        file_name: str,
        string_to_search: str
    ) -> bool:
        """
        @param {str} file_name The file in which we will look for the string occurrence.
        @param {str} string_to_search The string we are looking for in the file.

        Determines if the given string is present in the file. Useful to find warning messages
        in log files.

        @returns {bool}    
        """
        file_manager = FileManager(file_name)
        return file_manager.is_string_present_in_the_file(string_to_search)

    # Mehtods for specific files
    def get_value_from_snmpd(self, regex: str) -> str:
        """
        @param {str} regex The regular expression to search the value in SNMPD.

        Searches a value in the SNMPD conf file with a regular expression (ideally using the regex
        pattern (.*?) after the known key literal).

        @returns Desired value in file.
        """
        # We create a new file manager for the snmpd.conf file
        file_manager = FileManager(ESAFileManager.ESA_SNMPD_CONF_FILE_NAME)
        # We get the desired value using the regular expression
        return file_manager.search_value_with_regex(regex)

    def is_warning_present_in_the_logs(self, warning: str) -> bool:
        """
        @param {str} warning The warning message we are looking for in the logfile.

        Determines if a warning message - or pattern - is present in the logfile. Very useful
        to perform validations, because some issues expect certain messages in the logs to determine
        that the problems are due to that specific misconfiguration or error.

        @returns {bool}
        """
        return self.is_string_present_in_file(self.ESA_LOG_FILE_NAME, warning)

    # Methods to get relevant values for ESA

    def get_esa_serial_number(self) -> str:
        """
        Retrieves the serial number from the SNMPD file the first time, then the value in the local
        state will be returned to avoid reopening the file.

        @returns ESA's serial number.
        """
        if self.serial_number == None:
            self.serial_number = self.get_value_from_snmpd(r'Serial #: (.*)$')
        return self.serial_number

    def get_esa_version_number(self) -> str:
        """
        Retrieves the version number from the SNMPD file the first time, then the value in local
        state will be returned to avoid reopening the file.

        @returns ESA's AsyncOS version number.
        """
        if self.version_number == None:
            self.version_number = self.get_value_from_snmpd(r'AsyncOS Version: (.*?),')
        return self.version_number
    
    # General file utils

    def safely_remove_file(self, path_to_file: str):
        """
        @param {str} path_to_file The path to the file we want to delete.

        Removes a file via the FileManager, which performs a validation to assure that it'll only
        attempt to delete the file if it actually exists in the provided path.
        """
        FileManager(path_to_file).delete_file()


