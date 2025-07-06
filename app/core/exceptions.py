from typing import Union

class NotFoundError(Exception):
    """Exception raised when an entity is not found."""
    def __init__(self, entity: str, identifier: Union[int, str]) -> None:
        """
        Initialize the NotFoundError with the entity type and identifier.

        Example:
            ```python
            raise NotFoundError(entity="Candidate", identifier="12345")
            ```
            This will raise an exception with the message:
            ```txt
            NotFoundError: Candidate with identifier '12345' not found.
            ```
        """
        self.entity = entity
        self.identifier = identifier
        super().__init__(f"{entity} with identifier '{identifier}' not found.")

class InvalidCredentialsError(Exception):
    """Exception raised when authentication credentials are invalid."""
    def __init__(self, message: str = "Invalid credentials provided.") -> None:
        """
        Initialize the InvalidCredentialsError with a custom message.

        Example:
            ```python
            raise InvalidCredentialsError("The provided password is incorrect.")
            ```
        """
        super().__init__(message)

class UnexpectedError(Exception):
    """Exception raised for unexpected errors."""
    def __init__(self, message: str = "An unexpected error occurred.") -> None:
        """
        Initialize the UnexpectedError with a custom message.

        Example:
            ```python
            raise UnexpectedError("Something went wrong while processing the request.")
            ```
        """
        super().__init__(message)