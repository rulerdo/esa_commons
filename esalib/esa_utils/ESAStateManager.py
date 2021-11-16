
# ESA utils
from .ESASSHAgent import ESASSHAgent
from .ESAFileManager import ESAFileManager
# Validator
from .ESAVersionValidator import ESAVersionValidator
# Utils
from ..utils.logger.Logger import Logger


class ESAStateManager:
    """
    @version 1.4.1

    Container for the ESA state, storing relevant information about it, such as the serial number, tenant
    id or version number. It also provides methods to set automtically these values from the files managed
    by ESAFileManager.
    """

    def __init__(
        self, 
        ssh_agent: ESASSHAgent,
        esa_file_manager: ESAFileManager,
        supported_versions: list[str] = [],
    ):
        """
        @param {ESASSHAgent} Instance of the SSH agent for ESA. Generally there is one per use case.
        @param {ESAFileManager} Instance of the ESA file manager, to request remote files or values from those files.
        """
        self.ssh_agent: ESASSHAgent = ssh_agent
        self.esa_file_manager: ESAFileManager = esa_file_manager
        self.supported_versions: list[str] = supported_versions
        # Internal state
        self.tenant_id = None
        self.serial_number = ''
        self.version_number = ''

    # Facade
    def set_state_from_files(self):
        """
        Facade method to set the basic state (serial_number, version_number and tenant_id from files).
        It first requests the essential files from the ESA file manager, and invoke the methods that 
        retrieve the values from them (making use of the ESA file manager as well, because we do not 
        manage files directly in this class to be SRP compliant)
        """
        # We retrieve the essential ESA files using the ESAFileManager
        self.esa_file_manager.get_essential_files()
        # We get ESA's serial and version numbers
        self.set_serial_number_from_file()
        self.set_version_number_from_file()
        # We set the tenant_id value according to the value present in the config file
        self.set_tenant_id_from_file()
        
    # Methods to set state values

    def set_serial_number_from_file(self):
        """
        Saves the serial number to local state. The version number is retrieved from the SNMPD conf file.
        A validation is performed to guarantee that the value is not null, because this is a critical value
        for the whole remediation process.
        """
        Logger.info(f'Getting serial number from { ESAFileManager.ESA_SNMPD_CONF_FILE_NAME }')
        # We set the serial number in state
        self.serial_number = self.esa_file_manager.get_esa_serial_number()
        Logger.info(f'Device serial number: [{ self.serial_number }]')
        # We validate the serial number
        self.__is_valid_serial_number()

    def set_version_number_from_file(self):
        """
        Saves the version number to local state. The version number is retrieved from the SNMPD conf file. 
        A validation is performed to guarantee that the version number is supported by this implementation.
        """
        Logger.info(f'Getting version number from { ESAFileManager.ESA_SNMPD_CONF_FILE_NAME }')
        # We set the version number in state
        self.version_number = self.esa_file_manager.get_esa_version_number()
        Logger.info(f'Version number = { self.version_number }')
        # We validate the version number
        self.__is_valid_version_number()

    def set_tenant_id_from_file(self):
        """ 
        Sets the tenant_id value in local state. It obtains this value from ESA's config file using a
        regular expression.
        """
        # We use the ESAFileManager class, to request the value from the ESA config file
        tenant_id = self.esa_file_manager.get_value_from_file(
            ESAFileManager.ESA_CONFIG_FILE_NAME, 
            r'\{"tenant_id":"(.*?)"\}'
        )
        # We set the current tenant_id
        Logger.info(f'ESA tenant_id = [{ tenant_id }]')
        self.tenant_id = tenant_id

    # Validations

    def __is_valid_serial_number(self):
        """
        Method to determine if the serial number is not empty, raising an exception if thats the case, because
        this is a crucial component in the remediation process.
        """
        if self.serial_number == None:
            raise Exception('Serial number field not found')

    def __is_valid_version_number(self):
        """
        Method to determine if the version is valid and if it is currently supported by this TenantFix
        implementation. If it finds that the version is not supported, the execution will stop at this point.
        """
        # Version validation
        ESAVersionValidator(self.version_number, self.supported_versions).validate()

        if self.version_number == None:
            raise Exception('Version number field not found')


