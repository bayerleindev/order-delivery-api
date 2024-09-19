class CourierException(Exception):
    def __init__(self, error) -> None:
        self.error = error
