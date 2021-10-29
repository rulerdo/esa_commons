import unittest
# ESA utils
from esalib.esa_utils.ESASSHAgent import ESASSHAgent
from esalib.esa_utils.ESAParameters import ESASSHParameters
# Logger
from esalib.utils.logger.Logger import Logger


class SSHAgentTest(unittest.TestCase):

    @classmethod
    def setUp(self) -> None:
        # We initialize the logger
        Logger.initialize()
        # We create the SSH agent instance, providing the parameters
        self.ssh_parameters = ESASSHParameters('', '', '')
        self.esa_ssh_agent = ESASSHAgent(self.ssh_parameters)
        # We start the SSH connection
        self.esa_ssh_agent.start_connection()

    def test_connection(self):
        """Tests the connection object."""
        # We verify that the connection object is not null
        self.assertIsNotNone(self.esa_ssh_agent.ssh_connection)

    def test_command(self):
        """Test the method to execute a command and get the output."""
        output = self.esa_ssh_agent.execute_command('ls')
        self.assertIsNotNone(output)
        self.assertIsNot(output, '')

    def test_cli_command(self):
        """Test the method to execute a command at CLI level and get the output."""
        output = self.esa_ssh_agent.execute_cli_command('version')
        self.assertIsNotNone(output)
        self.assertIsNot(output, '')
    
if __name__ == '__main__':
    unittest.main()