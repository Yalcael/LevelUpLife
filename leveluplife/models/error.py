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


class UserUsernameNotFoundError(BaseError):
    def __init__(
        self,
        user_username: str,
        status_code: int = 404,
        name: str = "UserUsernameNotFoundError",
    ):
        self.name = name
        self.message = f"User with username {user_username} not found"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class UserEmailNotFoundError(BaseError):
    def __init__(
        self,
        user_email: str,
        status_code: int = 404,
        name: str = "UserEmailNotFoundError",
    ):
        self.name = name
        self.message = f"User with email {user_email} not found"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class TribeNotFoundError(BaseError):
    def __init__(
        self,
        tribe: str,
        status_code: int = 404,
        name: str = "TribeNotFoundError",
    ):
        self.name = name
        self.message = f"Tribe with the name {tribe} not found"
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


class TaskTitleNotFoundError(BaseError):
    def __init__(
        self,
        task_title: str,
        status_code: int = 404,
        name: str = "TaskTitleNotFoundError",
    ):
        self.name = name
        self.message = f"Task with title {task_title} not found"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class ItemAlreadyExistsError(BaseError):
    def __init__(
        self, _name: str, status_code: int = 409, name: str = "ItemAlreadyExistsError"
    ):
        self.name = name
        self.message = f"Item with the name {_name} already exists."
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class ItemNotFoundError(BaseError):
    def __init__(
        self, item_id: UUID, status_code: int = 404, name: str = "ItemNotFoundError"
    ):
        self.name = name
        self.message = f"Item with ID {item_id} not found"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )


class ItemNameNotFoundError(BaseError):
    def __init__(
        self,
        item_name: str,
        status_code: int = 404,
        name: str = "ItemNameNotFoundError",
    ):
        self.name = name
        self.message = f"Item with name {item_name} not found"
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )
