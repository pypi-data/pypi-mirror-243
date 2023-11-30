class TodotreeError(Exception):
    """
    Generic Exception class for application specific exceptions.
    """
    def __init__(self, message):
        self.message = message

        super().__init__(message)

    def __str__(self):
        return self.message
