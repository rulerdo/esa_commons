import os
import re
# Compressed files handler
from utils.files.compressed_files.CompressedFileManager import CompressedFileManager
# Utils
from utils.logger.Logger import Logger


class FileManager:
    """
    @version 1.6.2

    Class to handle the most common operations for files in a predictable and decoupled-from-implementation way.
    It also supports compressed files, handling the file according to it's extension making use of the 
    strategy pattern via the CompressedFileManager wrapper, which decides which strategy to use.
    """
    def __init__(
        self, 
        path_to_file,
    ):
        """
        @param {str} path_to_file The path to the file to manage.

        The file extension and file name are determined based on the provided path.
        """
        self.path_to_file = path_to_file
        self.file_name = ''
        self.file_extension = ''
        # We set the file extension internally
        self.__set_file_name()
        self.__set_file_extension()

    def open(self, mode = 'rt'):
        """
        @param {str} mode The file mode. The default mode is 'rt' because it allows compressed files to be iterated as strings and not bytes.
        @returns {FileIOWrapper} The opened file.

        Method to open a file and get the reference to it. It supports compressed files, applying 
        the concrete strategy to get the file content via the CompressedFileManager facade.
        """
        # We open the file normally if it is not compressed (this is indicated by the extension)
        if not self.__is_compressed_file():
            self.file = open(self.path_to_file, mode)
        # If the file is compressed, we manage it via the CompressedFileHandler
        else: 
            self.file = CompressedFileManager(
                path_to_file = self.path_to_file, 
                compression_type = self.file_extension
            ).open(mode)

        return self.file
    
    def close(self):
        """
        Method to close an open file.
        """
        if self.file:
            self.file.close()

    def delete_file(self):
        """
        Method to delete a file located in the given path after performing a validation to assure that
        the file exists.
        """
        if not self.file_exists():
            return
        os.remove(self.path_to_file)

    def rename_file(self, new_file_name: str):
        """
        @param {str} new_file_name String with the new name of the file.

        Method to rename the current file with a provided new name.
        """
        os.rename(self.file_name, new_file_name)
        
    def file_exists(self) -> bool:
        """
        Method that indicates if the file exists in the specified path.
        """
        return os.path.exists(self.path_to_file)

    def search_value_with_regex(self, regex: str) -> str:
        """
        @param {str} regex The regular expression in string format.
        @returns {str} The value of the desired pattern.

        Returns the value of the key provided as regex (ideally for a dictionary or JSON-like files)
        It is useful to get the values in a dictionary-like structured file.
        """
        return self.__search_with_regex(regex, search_value = True)
 
    def is_string_present_in_the_file(self, regex: str) -> bool:
        """
        @param {str} regex The regular expression in string format.
        @returns {bool} A boolean value that indicates if the string is present in the file or not.

        Returns the string if it is present in the file. The main difference with the search_value_with_regex
        method is that this one only validates if the given string is present in the file, but we don't want
        to retrieve any sort of result or value for it, other than the string ocurrence itself. 
        It is useful to validate if some kind of warning is present in logs or that kind of files. 
        """
        result = self.__search_with_regex(regex, search_value = False)
        return result != None

    def read_file_content(self, mode = 'rt'):
        """
        @param {str} mode The mode to open the file.

        Method to retrieve the content of the file, validating that the file is open before that.

        @returns {str} The file content.
        """
        # We open the file in the specified mode
        self.open(mode)
        # We retrieve the content and save it to a variable, not without validating that the file opened correctly
        self.__validate_file_is_open()
        content = self.file.read()
        # We close the file and return the content
        self.close()
        return content
        

    # Internal utils

    def __search_with_regex(
        self, 
        regex: str,
        search_value: bool = True,
    ):
        """
        @param {str} regex Regular expression.
        @param {bool} search_value Indicates if we are looking for a value (for a key-value pattern). If false, we only are looking for the ocurrence of the pattern.

        Method to retrieve either the value or the string ocurrence of a regex in a file.
        If the search_value flag is set to true, we are going to look for the value in a dictionary-like
        structure, like what we would do in a dictionary with dict[key].
        Otherwise, the pattern will only be searched in the file.
        """
        # We set the default result to False if the search_value flag is disabled, because we are looking for a bool value of the ocurrence
        result = None if not search_value else False
        expression = re.compile(regex)
        # We open and analyze the file, searching for the regex pattern
        self.open()
        for line in self.file:
            match = expression.search(line)
            if match != None:
                result = (
                    match.group(1) 
                        if search_value
                        else True
                )
                Logger.debug(f'Search with regex in file result = { result }')
                break
        # We close the file
        self.close()
        return result

    def __set_file_name(self):
        """
        Method to set the file name internally.
        """
        self.file_name = os.path.basename(self.path_to_file)

    def __set_file_extension(self):
        """
        Method to set the file extension internally.
        """
        _, file_extension = os.path.splitext(self.path_to_file)
        self.file_extension = file_extension

    def __is_compressed_file(self):
        """
        Method to determine if the file is compressed, by verifying if the file extension is present
        in the COMPRESSION_EXTENSIONS list of CompressedFileManager.
        """
        return self.file_extension in CompressedFileManager.COMPRESSION_EXTENSIONS

    def __validate_file_is_open(self):
        """
        Method to validate that the file is open, raising an exception if it's not.
        """
        if not self.file:
            raise Exception('The file is not open')


