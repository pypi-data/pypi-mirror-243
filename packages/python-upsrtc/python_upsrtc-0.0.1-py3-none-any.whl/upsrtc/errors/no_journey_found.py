
class NoJourneyFoundError(Exception):
    """
    Raised when no journey is found for a given search settings
    """
    def __init__(self, message):
        super().__init__(message)