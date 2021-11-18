import re
import time
# Services contract
from ..Service import Service
# ESA utils
from ....esa_utils.ESASSHAgent import ESASSHAgent
# Utils
from ....utils.validators.IteratorValidator import IteratorValidator

class HeimdallService(Service):
    """
    @version 1.0.0

    Implementation of the manager for the heimdall_svc service.
    """
    
    def __init__(
        self,
        esa_ssh_agent: ESASSHAgent
    ):
        # We call the parent constructor, providing the service path for this service and the ssh_agent
        super().__init__(
            service_path = '/data/bin/heimdall_svc',
            esa_ssh_agent = esa_ssh_agent,
        )

    def set_service_status(
        self, 
        service_name: str, 
        service_status: str, 
        sleep_time_after_command: float = 0.75
    ):
        """
        @param {str} service_name The name of the service to execute.
        @param {str} service_status The status that we want to set the service to.
        @param {str} sleep_time_after_command The time to wait after the command executes.

        Method to set a service to a certain status.
        """
        output = self.esa_ssh_agent.execute_command(
            f'{ self.service_path } -{ service_status } { service_name }'
        )
        # We wait the specified or default time and return the output
        time.sleep(sleep_time_after_command)
        return output

    def is_service_active(self, service_name: str) -> bool:
        """
        @param {str} service_name The name of the service to execute.

        Method to determine if the service is active via a regular expression to find a PID other than -1.
        """
        status = self.set_service_status(service_name, 's')
        regex = re.compile(r'\'pid\': (\-?\d+), ')
        service_pid = regex.findall(status).pop(0)
        return int(service_pid) > -1


    def wait_until_service_is_up(
        self, 
        service_name: str, 
        timeout: float = 20,
        sleep_time: float = 0.1
    ):
        """
        @param {str} service_name The name of the service to execute.

        Method to wait until a service is up and running. It only waits until the timeout is reached, then an exception is raised.
        """
        iterations_validator = IteratorValidator.iterator_with_timeout(timeout, sleep_time)
        while not self.is_service_active(service_name):
            next(iterations_validator)
        return
        
