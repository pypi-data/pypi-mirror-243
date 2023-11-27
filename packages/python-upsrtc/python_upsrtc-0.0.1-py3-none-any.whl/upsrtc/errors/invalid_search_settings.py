
class InvalidSearchSettingsError(Exception):
    """
    Raised when the search settings are invalid.
    """
    def __init__(self, message):
        super().__init__(message)