
class SSHConnection:
    """
    @version 1.1.1
    
    Class to manage the SSH connection as a Singleton instance, so that only a connection is created and 
    accessed even by multiple processes
    """
    # Connection instance (Singleton)
    __connection = None

    def set_connection(connection):
        """
        @param {object} connection The SSH connection reference.
        
        Method to set the connection in a Singleton way
        """
        SSHConnection.__connection = connection

    def get_connection():
        """
        Method to retrieve the connection instance. It validates the existance of this instance, so that we
        prevent the calling of methods or properties on a null instance

        @returns {object} SSH connection.
        """
        if not SSHConnection.__connection:
            raise Exception('No SSH connection instance')
        return SSHConnection.__connection