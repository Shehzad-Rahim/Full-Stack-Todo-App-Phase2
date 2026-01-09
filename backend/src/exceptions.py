from fastapi import HTTPException, status


class TaskNotFoundException(HTTPException):
    """
    Exception raised when a task is not found for a specific user.
    """
    def __init__(self, task_id: int, user_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found for user {user_id}"
        )


class UserNotFoundException(HTTPException):
    """
    Exception raised when a user is not found.
    """
    def __init__(self, user_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )


class ValidationErrorException(HTTPException):
    """
    Exception raised for validation errors.
    """
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )


class DatabaseConnectionException(HTTPException):
    """
    Exception raised for database connection issues.
    """
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error"
        )