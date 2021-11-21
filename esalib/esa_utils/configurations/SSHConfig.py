# Base configuration
from .BaseConfig import BaseConfig, BaseConfigOperations
# ESA utils
from ..ESASSHAgent import ESASSHAgent
# Utils
from ...utils.logger.Logger import Logger


class SSHAvailableConfigurations:
    """SSH available configuration options."""
    SSHD            = 'SSHD'
    USERKEY         = 'USERKEY'
    ACCESS_CONTROL  = 'ACCESS CONTROL'

class SSHAvailableOperations:
    """SSH available operations over the selected configuration."""
    SETUP           = BaseConfigOperations.SETUP
    CLUSTERSET      = 'CLUSTERSET'
    CLUSTERSHOW     = 'CLUSTERSHOW'

class SSHConfig(BaseConfig):
    """
    @version 1.0.0

    Class that provides methods to access and configure parameters in sshconfig mode. It extends the base class BaseConfig to add 
    methods specific to sshconfig mode.
    """

    # Constants
    AVAILABLE_OPERATIONS = SSHAvailableOperations
    AVAILABLE_CONFIGURATIONS = SSHAvailableConfigurations

    def __init__(
        self,
        esa_ssh_agent: ESASSHAgent,
        is_in_cluster_mode: bool = True,
    ):
        # We initialize the parent class
        super().__init__(
            esa_ssh_agent = esa_ssh_agent,
            config_mode_name = 'sshconfig',
            is_in_cluster_mode = is_in_cluster_mode
        )

    # Configurations

    def select_configuration(self, configuration: str):
        """
        @param {str} configuration The configuration to select.

        Method to select the configuration mode for SSH (AVAILABLE_CONFIGURATIONS). It increases the nested config level.
        """
        self.increase_nested_config_level()
        Logger.info(f'Entering to { configuration } configuration mode.')
        return self.introduce_configuration_value(configuration)
    
    def enter_to_sshd_configuration(self) -> str:
        """Method to enter to SSHD configuration."""
        return self.select_configuration(self.AVAILABLE_CONFIGURATIONS.SSHD)

    def enter_to_userkey_configuration(self) -> str:
        """Method to enter to USERKEY configuration."""
        return self.select_configuration(self.AVAILABLE_CONFIGURATIONS.USERKEY)

    def enter_to_access_control_configuration(self) -> str:
        """Method to enter to ACCESS CONTROL configuration."""
        return self.select_configuration(self.AVAILABLE_CONFIGURATIONS.ACCESS_CONTROL)

    # Operations

    def select_operation_to_apply(self, operation: str) -> str:
        """
        @param {str} operation Operation to apply.

        Method to apply an operation (AVAILABLE_OPERATIONS) to the selected configuration mode. It increases the nested config level.
        """
        self.increase_nested_config_level()
        Logger.info(f'Applying { operation } operation.')
        return self.introduce_configuration_value(operation)

    def apply_setup_operation(self) -> str:
        """Method to apply the SETUP operation."""
        return self.select_operation_to_apply(self.AVAILABLE_OPERATIONS.SETUP)

    def apply_cluster_setup_operation(self) -> str:
        """Method to apply the CLUSTERSET operation."""
        return self.select_operation_to_apply(self.AVAILABLE_OPERATIONS.CLUSTERSET)

    def apply_cluster_show_operation(self) -> str:
        """Method to apply the CLUSTERSHOW operation."""
        return self.select_operation_to_apply(self.AVAILABLE_OPERATIONS.CLUSTERSHOW)

    
    
