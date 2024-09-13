from route.repository import RouteRepository


class GetRouteOrders:

    def __init__(self) -> None:
        self.repository = RouteRepository()

    def execute(self, **kwargs):
        return self.repository.get_orders(**kwargs)
