# Utils
from ..utils.logger.Logger import Logger

class ESABaseRemediationStatusCodes:
    """
    @version 1.2.1

    Container of the status codes for the remediation and their corresponding message.
    It can be extended with more definitions.
    """
    # Codes
    ERROR = 100
    SUCCESS = 200

    # Messages
    messages: dict[int, str] = {
        ERROR: 'There was an error: <%s>',
        SUCCESS: 'The issue was solved successfully, all the steps were executed correctly.',
    }

    def append_messages(self, messages_dictionary: dict[int, str]):
        """
        @param {dict} messages_dictionary The dictionary containing the custom messages.

        Method to merge the initial dictionarey with the custom one.
        """
        self.messages = { **self.messages, **messages_dictionary }

    def get_message_by_status_code(self, status_code: int) -> str:
        """
        @param {int} status_code Status code whose message we want to retrieve.

        Method to retrieve the message for a certain status code.
        """
        return self.messages[status_code] if status_code in self.messages.keys() else ''


class ESARemediationStatus():
    """
    @version 1.3.0

    Class to keep track of the remediation status via status codes. It also allows to keep track of the 
    files that were modified, which are candidates to be incorporated to the mail that is sent at the end
    of the process. 
    """

    def __init__(
        self, 
        custom_status_codes: ESABaseRemediationStatusCodes = None
    ):
        """
        @param {ESABaseRemediationStatusCodes} custom_status_codes Extended definition of status codes with custom messages and code numbers.
        """
        self.files: list[str] = []
        self.messages = { }
        self.custom_status_codes = custom_status_codes if custom_status_codes != None else ESABaseRemediationStatusCodes()

    # Setters

    def push_status_code(self, status_code: int):
        """
        @param {int} status_code Remediation status code.

        Appends a status code to the dictionary.
        """
        self.__add_code_to_dictionary(status_code)

    def push_and_log_status_code(self, status_code: int):
        """
        @param {int} status_code Remediation status code.

        Appends a status code to the dictionary and logs it's message.
        """
        self.push_status_code(status_code)
        Logger.info(self.custom_status_codes.get_message_by_status_code(status_code))

    def push_obtained_file(self, file_name: str):
        """
        @param {str} file_path The path to the retrieved file.

        Appends an obtained file path to the list.
        """
        self.__add_file_to_list(file_name)

    def push_uploaded_file(self, file_path: str):
        """
        @param {str} file_path The path to the uploaded file.

        Appends an uploaded (and therefore, modified) file path to the list.
        """
        self.__add_file_to_list(file_path)
    
    def set_error_message(self, error_message: str):
        """
        @param {str} error_message Error message string.

        Sets the specific error message to incorporate, it will fill the missing part of the generic error message.
        """
        error_key = ESABaseRemediationStatusCodes.ERROR
        self.messages[error_key] = self.custom_status_codes.get_message_by_status_code(error_key) % error_message

    # Facade

    def get_remediation_messages(self):
        """
        Returns a string with all the remediation messages joined by new line characters.
        Suitable for email body.
        """
        return '\n'.join(value for value in self.messages.values())

    def get_remediation_attachments(self) -> list[str]:
        """
        Returns the list of file paths that were retrieved or updated during the remediation process.
        Suitable for email attachments.
        """
        return self.files


    # Private methods

    def __add_file_to_list(self, file_path: str):
        """
        @param {str} file_path Path to the file to add.

        Method to push a non-existing file path to the list.
        """
        # If the file path already exists, we skip it
        if file_path in self.files:
            return
        self.files.append(file_path)
        

    def __add_code_to_dictionary(self, status_code: int):
        """
        @param {int} status_code Remediation status code to add.

        Method to add a code to the dictionary.
        """
        self.messages[status_code] = self.custom_status_codes.get_message_by_status_code(status_code)