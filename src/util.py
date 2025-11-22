"""Utility helpers for validating citation input."""


class UserInputError(Exception):
    """Exception raised for invalid user input in forms."""


def validate_citation(content):
    """Validate citation content length.

    Raises `UserInputError` when the content is shorter than 5
    or longer than 100 characters.
    """
    if len(content) < 5:
        raise UserInputError("Citation content length must be greater than 4")

    if len(content) > 100:
        raise UserInputError("Citation content length must be smaller than 100")
