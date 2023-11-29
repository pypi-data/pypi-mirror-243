
class NotifyAllError(Exception):
    """Base class for all exceptions in NotifyAll"""
    pass


class ConfigurationError(NotifyAllError):
    """Exception raised for errors in the configuration process"""
    pass


class UnsupportedChannelError(NotifyAllError):
    """Exception raised when an unsupported notification channel is used"""
    pass


class NotificationSendError(Exception):
    """
    Exception raised when sending a notification fails.

    Attributes:
        service_name -- name of the notification service (e.g., 'Telegram')
        original_exception -- the original exception that was raised
    """
    def __init__(self, service_name, original_exception):
        self.service_name = service_name
        self.original_exception = original_exception
        message = f"Failed to send notification via {service_name}: {original_exception}"
        super().__init__(message)