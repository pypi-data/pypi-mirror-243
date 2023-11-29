class BaseNotifier:
    def send_notification(self, params):
        raise NotImplementedError("This method should be implemented by subclasses.")
