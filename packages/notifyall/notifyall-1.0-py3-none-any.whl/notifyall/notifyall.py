import yaml
import logging
import os

from .exceptions import ConfigurationError
from .notification_manager import NotificationManager


class NotifyAll:

    def validate_config(self, config):
        notifiers = config.get('notifyall')
        for notifier in list(notifiers.keys()):
            if 'telegram' in notifier:
                if not notifiers.get('telegram').get('token'):
                    config.get('notifyall').pop('telegram')
                    self.logger.exception("Telegram token is missing in configuration")
                    raise ConfigurationError("Telegram token is missing in configuration")
            if 'sns' in notifier:
                if not notifiers.get('sns').get('default_phone_number'):
                    config.get('notifyall').pop('sns')
        return config

    # noinspection PyMethodMayBeStatic
    def load_config_from_env(self):
        """
        Load the configuration from a YAML file.

        Returns:
            dict: The configuration data loaded from the environment variables.

        """
        # Load configuration from environment variables
        self.config = {
            'notifyall': {
                'telegram': {
                    'token': os.getenv('TELEGRAM_TOKEN')
                },
                'sns': {
                    'default_phone_number': os.getenv('SNS_DEFAULT_NUMBER')
                }
            }
        }
        return self.validate_config(self.config)

    def load_config_from_file(self, file_path):
        """
            Load the configuration from a YAML file.
            Args:
                file_path (str): The path to the configuration file.
            Returns:
                dict: The configuration data loaded from the file.
            Raises:
                ConfigurationError: If the configuration file does not exist.
        """
        # Check if the configuration file exists
        if not os.path.exists(file_path):
            # Raise a ConfigurationError if the file is not found
            self.logger.exception("Configuration file not found")
            raise ConfigurationError(f"Configuration file not found: {file_path}")

        # Read and parse the YAML file
        with open(file_path, 'r') as file:
            self.config = yaml.safe_load(file)
        return self.validate_config(self.config)

    def __init__(self, config_file=None):
        """
            Initialize NotifyAll either with a configuration file or environment variables.

            Args:
                config_file (str, optional): Path to the YAML configuration file.
                    If None, configuration is loaded from environment variables.

            Raises:
                ConfigurationError: If both the configuration file and environment variables are missing or invalid.
        """
        # Initialize the logger for this class
        self.logger = logging.getLogger(__name__)
        # Log an informational message upon initialization
        self.logger.info('Initializing NotifyAll')

        # Attempt to load the configuration
        if config_file:
            self.config = self.load_config_from_file(config_file)
        else:
            self.config = self.load_config_from_env()

        if not self.config:
            raise ConfigurationError("Failed to load configuration from both file and environment variables")

        # Initialize the NotificationManager with the loaded configuration
        self.notification_manager = NotificationManager(self.config.get('notifyall'))

    def send(self, message, params):
        """
            Send a message using the specified parameters.
            Args:
                message (str): The message to be sent.
                params (object): Parameters specific to the notification channel.
        """
        # Delegate the sending action to the NotificationManager
        self.notification_manager.send(message, params)
