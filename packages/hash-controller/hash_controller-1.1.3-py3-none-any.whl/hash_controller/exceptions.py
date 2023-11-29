class DataBaseNotExistException(BaseException):
    def __init__(self) -> None:
        super().__init__("Database type not in env var")


class DataBaseNotConfigured(BaseException):
    def __init__(self, database: str = "") -> None:
        super().__init__(f"Database {database} not configured")
