from typing import Any
from db_config import mongo


class GeolocationRepository:

    def save_order_geolocation(
        self,
        order_number: str,
        courier_id: str,
        latest_location: Any,
        status: str = "BUSY",
    ):
        mongo.courier_locations.insert_one(
            {
                "_id": courier_id,
                "latest_location": {
                    "type": "Point",
                    "coordinates": [
                        float(latest_location["longitude"]),
                        float(latest_location["latitude"]),
                    ],
                },
                "locations": [latest_location],
                "status": status,
                "order_number": order_number,
            }
        )

    def get_order_geolocation(self, order_number: str):
        return mongo.courier_locations.find_one({"order_number": order_number})

    def get_courier_geolocation(self, courier_id: str):
        return mongo.courier_locations.find_one({"_id": courier_id})

    def update_order_geolocation(
        self,
        courier_id: str,
        order_number: str,
        latest_location: Any,
        locations: Any,
        status: str,
    ):
        mongo.courier_locations.update_one(
            {"_id": courier_id},
            {
                "$set": {
                    "latest_location": {
                        "type": "Point",
                        "coordinates": [
                            float(latest_location["longitude"]),
                            float(latest_location["latitude"]),
                        ],
                    },
                    "locations": locations,
                    "status": status,
                    "order_number": order_number,
                }
            },
        )
