from abc import ABCMeta, abstractmethod
# ESA utils
from .ESASSHAgent import ESASSHAgent
from .ESAParameters import ESAParameters
from .ESAFileManager import ESAFileManager
from .ESAStateManager import ESAStateManager
from .ESARemediationStatus import ESARemediationStatus, ESABaseRemediationStatusCodes
# Utils
from ..utils.logger.Logger import Logger
from ..utils.mail.CaseMailer import CaseMailer


class ESARemediationUseCase():
    """
    version 1.2.0
    
    Contract for the remediation use cases, it specifies the methods that must be implemented, as well as the parameters that they receive.
    """
    __metaclass__ = ABCMeta

    # Constructor, it receives the ESA utils initialized instances.
    @abstractmethod
    def __init__(
        self, 
        esa_ssh_agent: ESASSHAgent,
        esa_file_manager: ESAFileManager,
        esa_state_manager: ESAStateManager,
        esa_remediation_status: ESARemediationStatus
    ): raise NotImplementedError

    #Use case entry point
    @abstractmethod
    def solve(*args, **kwargs): raise NotImplementedError


class ESAManager:
    """
    @version 1.4.0
    
    Class to initialize all ESA services for the remediation use cases. It starts the SSH connections, retrieves the basic files and
    sets the ES state from the values in those files. Finally, the remediation status manager is initialized with the custom status codes.
    """
    def __init__(
        self,
        esa_parameters: ESAParameters,
        supported_versions: list[str],
        custom_status_codes: ESABaseRemediationStatusCodes,
    ):
        self.esa_parameters: ESAParameters = esa_parameters
        self.supported_versions: list[str] = supported_versions
        self.custom_status_codes: ESABaseRemediationStatusCodes = custom_status_codes
        # To be initialized
        self.esa_ssh_agent: ESASSHAgent = None
        self.esa_file_manager: ESAFileManager = None
        self.esa_state_manager: ESAStateManager = None
        self.esa_remediation_status: ESARemediationStatus = None

    def execute_use_case_remediation(self, remediation_use_case, *args, **kwargs):
        """
        @param {class} remediation_use_case The remediation use case class (without creating an instance of it, example: UseCase, instead of UseCase())

        Entry point for the use case. It calls all the required methods to remediate the issue.
        """
        try:
            # We initialize the ESA state manager
            self.__load()
            # We perform the remediations 
            self.remediation_use_case: ESARemediationUseCase = remediation_use_case(*self.__get_esa_utils())
            self.remediation_use_case.solve(*args, **kwargs)
        # We handle the exception, displaying the error message and ending the process
        except Exception as exception:
            self.__report_exception(exception)
        finally:
            # We send the case email if indicated
            self.__send_remediation_email()
            # Finally, we delete the retrieved files from ESA, as they are no longer required
            if self.esa_file_manager != None:
                self.esa_file_manager.remove_essential_files()
    
    # Internal methods

    def __load(self):
        """
        Entry point for the facade. It calls all the required methods to initialize the services.
        """
        # We start the connection with the ESA via SSH
        self.__start_ssh_connection()
        # We initialize the ESA state manager
        self.__initialize_esa_state()
    
    def __get_esa_utils(self):
        """Returns all the initialized ESA utils"""
        return (
            self.esa_ssh_agent, 
            self.esa_file_manager, 
            self.esa_state_manager, 
            self.esa_remediation_status
        )

    def __report_exception(self, exception: Exception):
        """Reports an exception at logger and remediation status level."""
        Logger.exception(exception.__str__())
        if self.esa_remediation_status != None:
            self.esa_remediation_status.push_status_code(self.custom_status_codes.ERROR)
            self.esa_remediation_status.set_error_message(exception.__str__())
        
    def __start_ssh_connection(self):
        """
        Starts the SSH connection with ESA via the ESASSHAgent class.
        """
        self.esa_ssh_agent = ESASSHAgent(self.esa_parameters.esa_ssh_parameters)
        self.esa_ssh_agent.start_connection()
    
    def __initialize_esa_state(self):
        """
        We initialize the ESA state. To do that, we need to create a single ESAFileManager instance to keep
        it across the whole use case, because we are going to take advantage of the caching, to avoid file 
        reopening and re-retrieval.
        Then, we create the state manager - as well, one per use case -, and initialize it from the files
        content via the set_state_from_files method.
        """
        # We create a file manager (required for ESAStateManager)
        self.esa_file_manager = ESAFileManager(self.esa_ssh_agent)
        # We create the ESAStateManager and initialize it
        self.esa_state_manager = ESAStateManager(self.esa_ssh_agent, self.esa_file_manager, self.supported_versions)
        self.esa_state_manager.set_state_from_files()
        # We initialize the remediation status container
        self.esa_remediation_status: ESARemediationStatus = ESARemediationStatus(
            self.custom_status_codes
        )

    def __send_remediation_email(self):
        """
        Sends a remediation mail if indicated by the send_case_email_flag. It gets it's body from the remediation
        status instance, which assigns the correct payload based on the status code. Also, the files are attached.
        """
        if not self.esa_parameters.esa_email_parameters.send_case_email:
            return
        CaseMailer(
            esa_status = self.esa_remediation_status,
            esa_email_parameters = self.esa_parameters.esa_email_parameters
        ).send_mail()
