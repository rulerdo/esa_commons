import gzip
# STrategy contract
from .CompressedFileStrategy import CompressedFileStrategy

class GZIPStrategy(CompressedFileStrategy):
    """
    @version 1.2.0

    Concrete implementation of the CompressedFileStrategy for GZIP files.
    """
    # Constructor
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    # Implementation of the open method for the GZIP files
    def open(self, *args, **kwargs):
        self.file = gzip.open(self.path_to_file, *args, **kwargs)
        return self.file