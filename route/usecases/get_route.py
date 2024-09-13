from route.repository import RouteRepository


class GetRoute:

    def __init__(self) -> None:
        self.repository = RouteRepository()

    def execute(self, **kwargs):
        return self.repository.get_route(**kwargs)
