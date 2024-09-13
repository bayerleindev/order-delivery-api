from order.repository import OrderRepository


class LoadOrder:
    def __init__(self) -> None:
        self.repository = OrderRepository()

    def execute(self, number: str):
        return self.repository.load(number)
