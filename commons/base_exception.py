class CustomBaseException(Exception):
    def __init__(self, error) -> None:
        super().__init__(error)
        self.error = error
