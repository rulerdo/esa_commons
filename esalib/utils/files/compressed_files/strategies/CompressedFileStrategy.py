from abc import ABCMeta, abstractmethod

class CompressedFileStrategy:
    """
    @version 1.3.0
    
    Interface that specifies the contract for the strategies that will handle each kind of compressed file.
    """
    __metaclass__ = ABCMeta

    # Constructor, it receives a path to the file.
    @abstractmethod
    def __init__(
        self, 
        path_to_file
    ): raise NotImplementedError

    # Method to open and return the reference to the file
    @abstractmethod
    def open(
        self, 
        path_to_file, 
        *args, 
        **kwargs
    ): raise NotImplementedError

