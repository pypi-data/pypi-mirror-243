import logging

from notifyall.exceptions import UnsupportedChannelError, ConfigurationError
from notifyall.notifiers.sns_notifier import SNSNotifier
from notifyall.notifiers.telegram_notifier import TelegramNotifier


class NotificationManager:
    def __init__(self, config):
        """
        Initialize the NotificationManager with configuration settings.

        This manager holds a dictionary mapping parameter class names to their
        respective notifier instances, allowing dynamic dispatch based on the
        type of parameters passed to the `send` method.
        Args:
            config (dict): Configuration data for the notification channels.
        """
        # Initialize the logger for this class
        self.logger = logging.getLogger(__name__)
        self.notifiers = {}

        # Initialize TelegramNotifier only if telegram configuration is present
        if 'telegram' in config:
            self.notifiers['TelegramParams'] = TelegramNotifier(config['telegram'])

        # Initialize SlackNotifier only if slack configuration is present
        if 'sns' in config:
            self.notifiers['SNSParams'] = SNSNotifier(config['sns'])

        # ... similarly for other notifiers

    def send(self, message, params):
        """
        Send a message using the specified notification channel.

        The method determines the appropriate notifier to use based on the
        type of the `params` object and delegates the message sending to that notifier.

        Args:
            message (str): The message to be sent.
            params (object): An instance of the parameters class for the specific
            notification channel (e.g., TelegramParams, SlackParams).

        Raises:
            ValueError: If no notifier is found for the provided parameter type.
        """
        # Determine the notifier based on the type of params object
        notifier_type = type(params).__name__
        if notifier_type in self.notifiers:
            # Call the send_notification method of the corresponding notifier
            self.notifiers[notifier_type].send_notification(params, message)
        else:
            # Handle the case where the notifier is not configured
            self.logger.exception("Unsupported notification channel or notifier was bad configured")
            raise UnsupportedChannelError(f"Unsupported notification channel: {type(params).__name__}")

