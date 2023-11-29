import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from requests import RequestException

from notifyall.exceptions import ConfigurationError, NotificationSendError
from notifyall.notification_manager import NotificationManager
from notifyall.notifiers.sns_notifier import SNSNotifier
from notifyall.notifiers.telegram_notifier import TelegramNotifier
from notifyall.notifyall import NotifyAll
from notifyall.params.sns_params import SNSParams
from notifyall.params.telegram_params import TelegramParams


class TestNotifyAll(unittest.TestCase):

    def test_initialization_with_valid_config(self):
        config = {'token': 'test_token'}
        notifier = TelegramNotifier(config)
        self.assertEqual(notifier.token, 'test_token')

    def test_initialization_with_invalid_config(self):
        with self.assertRaises(ConfigurationError):
            TelegramNotifier({})

    @patch('notifyall.notification_manager.TelegramNotifier')
    def test_initializes_telegram_notifier(self, mock_telegram_notifier):
        config = {'telegram': {'token': 'test_token'}}
        NotificationManager(config)
        mock_telegram_notifier.assert_called_once_with(config['telegram'])

    @patch('notifyall.notifyall.NotificationManager')
    def test_send_delegates_to_notification_manager(self, mock_notification_manager):
        mock_manager = mock_notification_manager.return_value
        notify_all = NotifyAll('tests/resources/config_test.yaml')
        notify_all.send("Test Message", MagicMock())
        mock_manager.send.assert_called_once()

    @patch('notifyall.notifyall.NotificationManager')
    def test_send_delegates_to_notification_manager_error(self, mock_notification_manager):
        mock_notification_manager.return_value
        with self.assertRaises(ConfigurationError):
            notify_all = NotifyAll()
            notify_all.send("Test Message", MagicMock())

    @patch('notifyall.notifyall.NotificationManager')
    def test_config_file_not_found(self, mock_notification_manager):
        mock_manager = mock_notification_manager.return_value
        with self.assertRaises(ConfigurationError):
            notify_all = NotifyAll('tests/resources/config_None.yaml')
            notify_all.send("Test Message", MagicMock())
            mock_manager.send.assert_called_once()

    def test_telegram_message_missing_raises_configuration_error(self):
        config = {'token': 'test_token'}
        params = TelegramParams(chat_id="123456789")
        notifier = TelegramNotifier(config)
        with self.assertRaises(ConfigurationError):
            notifier.send_notification(params, message=None)

    def test_telegram_chat_id_missing_raises_configuration_error(self):
        config = {'token': 'test_token'}
        params = TelegramParams(chat_id=None)
        notifier = TelegramNotifier(config)
        with self.assertRaises(ConfigurationError):
            notifier.send_notification(params, "message")

    def test_telegram_raises_request_exception(self):
        config = {'token': 'test_token'}
        params = TelegramParams(chat_id='chatid')
        notifier = TelegramNotifier(config)
        with self.assertRaises(NotificationSendError):
            notifier.send_notification(params, "message")

    def test_sns_message_missing_raises_configuration_error(self):
        config = {'default_phone_number': '123456789'}
        params = SNSParams(phone="123456789")
        notifier = SNSNotifier(config)
        with self.assertRaises(ConfigurationError):
            notifier.send_notification(params, message=None)

    def test_sns_default_number_missing_raises_configuration_error(self):
        config = {}
        params = SNSParams(phone=None)
        with self.assertRaises(ConfigurationError):
            notifier = SNSNotifier(config)


if __name__ == '__main__':
    unittest.main()
