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

        geolocation = self.repository.get_courier_geolocation(
            "COURIER_ID#{}".format(courier_id)
        )

        coordinates = Coordinates()

        coordinates.latitude = kwargs["latest_location"]["latitude"]
        coordinates.longitude = kwargs["latest_location"]["longitude"]

        if geolocation:
            geolocation["locations"].append(coordinates.to_json())
            self.repository.update_courier_geolocation(
                "COURIER_ID#{}".format(courier_id),
                coordinates.to_json(),
                geolocation["locations"],
            )
        else:
            self.repository.save_courier_geolocation(
                "COURIER_ID#{}".format(courier_id),
                courier_id,
                coordinates.to_json(),
                "FREE",
            )
