"""Exceptions raised by AndelaEatsAPI."""


class InvalidAuthTokenError(Exception):
    """Custom exception for handling invalid auth token."""

    def __init__(self, token_id):
        """Return error with customised message."""
        self.token_id = token_id
        super().__init__(f"Invalid aith key")
