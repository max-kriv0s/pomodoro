class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "User not correct login or password"


class TokenExpiredException(Exception):
    detail = "Token has expired"


class TokenNotCorrectException(Exception):
    detail = "Token is not correct"


class TaskNotFoundExeption(Exception):
    detail = "Task not found"
