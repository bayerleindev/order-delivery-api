from geolocation.repository import GeolocationRepository


class GetOrderGeolocation:

    def __init__(self) -> None:
        self.repository = GeolocationRepository()

    def execute(self, order_number: str):
        coordinates = self.repository.get_order_geolocation(order_number)[
            "latest_location"
        ]["coordinates"]

        return {"latitude": coordinates[1], "longitude": coordinates[0]}
