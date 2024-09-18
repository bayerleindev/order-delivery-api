from typing import Any
from geolocation.repository import GeolocationRepository


class Coordinates:
    latitude: str
    longitude: str

    def to_json(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
        }


class SaveGeolocation:

    def __init__(self) -> None:
        self.repository = GeolocationRepository()

    def execute(self, **kwargs):

        courier_id = kwargs["courier_id"]
        order_number = kwargs.get("order_number", None)

        self.update_order_geolocation(
            order_number,
            courier_id,
            latest_location=kwargs["latest_location"],
        )
        # else:
        #     geolocation = self.repository.get_courier_geolocation(
        #         "COURIER_ID#{}".format(courier_id)
        #     )

        #     coordinates = Coordinates()

        #     coordinates.latitude = kwargs["latest_location"]["latitude"]
        #     coordinates.longitude = kwargs["latest_location"]["longitude"]

        #     if geolocation:
        #         geolocation["locations"].append(coordinates.to_json())
        #         self.repository.update_courier_geolocation(
        #             "COURIER_ID#{}".format(courier_id),
        #             coordinates.to_json(),
        #             geolocation["locations"],
        #         )
        #     else:
        #         self.repository.save_courier_geolocation(
        #             "COURIER_ID#{}".format(courier_id),
        #             courier_id,
        #             coordinates.to_json(),
        #             "FREE",
        #         )

    def update_order_geolocation(
        self, order_number: str, courier_id: str, latest_location: Any
    ):
        geolocation = self.repository.get_courier_geolocation(courier_id)

        coordinates = Coordinates()

        coordinates.latitude = latest_location["latitude"]
        coordinates.longitude = latest_location["longitude"]

        if geolocation:
            geolocation["locations"].append(coordinates.to_json())
            self.repository.update_order_geolocation(
                courier_id,
                order_number,
                coordinates.to_json(),
                geolocation["locations"],
                status="BUSY" if order_number else "FREE",
            )
        else:
            self.repository.save_order_geolocation(
                order_number,
                courier_id,
                coordinates.to_json(),
                status="BUSY" if order_number else "FREE",
            )
