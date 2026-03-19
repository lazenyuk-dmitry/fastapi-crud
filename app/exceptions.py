class AppError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

class UserNotFoundError(AppError):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")

class UserAlreadyExistsError(AppError):
    def __init__(self):
        super().__init__(status_code=400, detail="Email already registered")

class IncorrectEmailOrPasswordError(AppError):
    def __init__(self):
        super().__init__(status_code=400, detail="Incorrect email or password")

class InvalidTokenError(AppError):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid token")

class InvalidCredentialsError(AppError):
    def __init__(self):
        super().__init__(status_code=401, detail="Could not validate credentials")

class OnlyForAdminError(AppError):
    def __init__(self):
        super().__init__(status_code=403, detail="Only admins can do this")

class OnlyForOwnerError(AppError):
    def __init__(self):
        super().__init__(status_code=403, detail="You can only access your own data")

class InactiveUserError(AppError):
    def __init__(self):
        super().__init__(status_code=403, detail="User is inactive")
