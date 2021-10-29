# Strategy contract
from .strategies.CompressedFileStrategy import CompressedFileStrategy
# Strategies
from .strategies.GZIPStrategy import GZIPStrategy

class CompressedFileManager:
    """
    @version 1.1.3

    Class to open and get the reference to compressed files, it makes use of the strategy pattern to apply
    the corresponding algorithm or implementation based on the compression type.
    """
    # Compression types
    GZ = '.gz'
    ZIP = '.zip'

    # List of supported compression extensions
    COMPRESSION_EXTENSIONS = [GZ, ZIP]

    # Strategies dictionary
    COMPRESSION_HANDLERS = {
        GZ: GZIPStrategy,
        ZIP: GZIPStrategy
    }

    def __init__(
        self, 
        path_to_file: str, 
        compression_type: str
    ):
        """
        @param {str} path_to_file String that contains the path to the file.
        @param {str} compression_type String that indicates the compression type of the file.
        """
        self.strategy: CompressedFileStrategy = None
        self.path_to_file = path_to_file
        self.compression_type = compression_type
        
    def open(self, *args, **kwargs):
        """
        Method to open and get the reference to the file via the corresponding strategy for the 
        compression type.
        """
        # We set the implementation to used based on the provided compression type parameter
        self.__set_strategy_to_apply()
        return self.strategy.open(*args, **kwargs)

    def __set_strategy_to_apply(self):
        """
        Method to set the strategy to apply internally. A validation of the existance of the strategy
        for the compression type is performed previuosly.
        """
        # We validate that the compression type exists in the dictionary
        if not self.compression_type in self.COMPRESSION_HANDLERS:
            raise Exception('There is no implementation available for the provided compression type')
        # We get the strategy to apply and return it
        self.strategy = self.COMPRESSION_HANDLERS[self.compression_type](self.path_to_file)
        


