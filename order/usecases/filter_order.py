from order.repository import OrderRepository


class FilterOrder:
    def __init__(self) -> None:
        self.repository = OrderRepository()

    def execute(self, **kwargs):
        return self.repository.filter(**kwargs)
