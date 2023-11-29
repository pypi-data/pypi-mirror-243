import logging

import requests

from notifyall.exceptions import ConfigurationError, NotificationSendError
from notifyall.notifiers.base_notifier import BaseNotifier


class TelegramNotifier(BaseNotifier):

    def __init__(self, config):
        # Initialize the logger for this class
        self.logger = logging.getLogger(__name__)
        # Initialize the notifier with specific configuration
        self.token = config.get('token')
        if not self.token:
            self.logger.exception("Telegram token is missing in configuration")
            raise ConfigurationError("Telegram token is missing in configuration")
        self.api_url = f"https://api.telegram.org/bot{self.token}/"
        # ... other Telegram-specific configuration

    def send_notification(self, params, message=None):
        if not message:
            self.logger.exception("Telegram message is missing in configuration")
            raise ConfigurationError("Telegram message is missing in configuration")

        chat_id = params.chat_id
        if not chat_id:
            self.logger.exception("Telegram chat_id is missing in Params configuration")
            raise ConfigurationError("Telegram chat_id is missing in Params configuration")
        method = 'sendMessage'
        url = f"{self.api_url}{method}"
        data = {'chat_id': chat_id, 'text': message}

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            self.logger.info("Message sent successfully")
        except requests.exceptions.RequestException as e:
            if e.response.status_code == 400:
                self.logger.error("Please check your chat_id.")
            elif e.response.status_code == 404:
                self.logger.error("Please check your token.")
            self.logger.error(f"An error occurred: {e}")
            raise NotificationSendError('Telegram', e)
