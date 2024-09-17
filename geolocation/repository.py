from typing import Any
from db_config import mongo


class GeolocationRepository:
    def get_courier_geolocation(self, id: str):
        return mongo.orders.find_one({"_id": id})

    def update_courier_geolocation(self, id: str, latest_location: Any, locations: Any):
        mongo.orders.update_one(
            {"_id": id},
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
                }
            },
        )

    def save_courier_geolocation(
        self, courier_id: str, latest_location: Any, status: str = "BUSY"
    ):
        mongo.orders.insert_one(
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
            }
        )
