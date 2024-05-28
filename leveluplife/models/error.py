class BaseError(Exception):
    def __init__(self, name: str, message: str, status_code: int):
        self.name = name
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UserAlreadyExistsError(BaseError):
    def __init__(
        self, email: str, status_code: int = 409, name: str = "UserAlreadyExistsError"
    ):
        self.name = name
        self.message = f"User with the email {email} already exists."
        self.status_code = status_code
        super().__init__(
            name=self.name, message=self.message, status_code=self.status_code
        )
