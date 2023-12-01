"""
This module contains custom exceptions for the orodha keycloak package.
"""
class InvalidConnectionException(Exception):
    """
    Exception for when connection arguments are missing or invalid

    Args:
        missing_args(list[str]): A list of the missing argument keys.
        message(str): An optional message to be displayed when raised.
    """

    def __init__(self, missing_args: list, message: str = None):
        if message is None:
            message = "Missing connection args:"
            for arg in missing_args:
                message += f" {arg}"
            super().__init__(message)
        self.message = message
