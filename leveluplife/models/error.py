from uuid import UUID


class BaseError(Exception):
    def __init__(self, name: str, message: str, status_code: int):
        self.name = name
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UserEmailAlreadyExistsError(BaseError):
    def __init__(
        self,
        email: str,
        status_code: int = 409,
        name: str = "UserEmailAlreadyExistsError",
    ):
        self.name = name
        self.message = f"User with the email {email} already exists."
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class UserUsernameAlreadyExistsError(BaseError):
    def __init__(
        self,
        username: str,
        status_code: int = 409,
        name: str = "UserUsernameAlreadyExistsError",
    ):
        self.name = name
        self.message = f"User with the username {username} already exists."
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class UserNotFoundError(BaseError):
    def __init__(
        self, user_id: UUID, status_code: int = 404, name: str = "UserNotFoundError"
    ):
        self.name = name
        self.message = f"User with ID {user_id} not found"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class TaskAlreadyExistsError(BaseError):
    def __init__(
        self, title: str, status_code: int = 409, name: str = "TaskAlreadyExistsError"
    ):
        self.name = name
        self.message = f"Task with the title {title} already exists."
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class TaskNotFoundError(BaseError):
    def __init__(
        self, task_id: UUID, status_code: int = 404, name: str = "TaskNotFoundError"
    ):
        self.name = name
        self.message = f"Task with ID {task_id} not found"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )
