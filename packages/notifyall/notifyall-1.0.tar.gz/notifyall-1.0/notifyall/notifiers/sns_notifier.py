import logging
import boto3
from botocore.exceptions import BotoCoreError, ClientError

from notifyall.exceptions import ConfigurationError, NotificationSendError
from notifyall.notifiers.base_notifier import BaseNotifier


class SNSNotifier(BaseNotifier):

    def __init__(self, config):
        # Initialize the logger for this class
        self.logger = logging.getLogger(__name__)
        self.client = boto3.client('sns')

        # Initialize the notifier with specific configuration
        self.default_phone_number = config.get('default_phone_number')
        if not self.default_phone_number:
            self.logger.exception("SNS default number is missing in configuration")
            raise ConfigurationError("SNS default number is missing in configuration")

    def send_notification(self, params, message=None):
        if not message:
            self.logger.exception("SNS message is missing in configuration")
            raise ConfigurationError("SNS message is missing in configuration")
        try:
            # Use the default phone number if none is provided
            phone_number = params.phone or self.default_phone_number
            self.client.publish(PhoneNumber=phone_number, Message=message)
            self.logger.info("Message sent successfully")
        except (BotoCoreError, ClientError) as e:
            self.logger.error(f"Failed to send SMS via SNS: {e}")
            raise NotificationSendError('SNS', e)

