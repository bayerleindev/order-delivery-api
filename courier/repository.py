from typing import List
from courier.model import CourierModel
from db_config import db_session, mongo


class CourierRepository:
    def save(self, courier: CourierModel):
        db_session.add(courier)

    def find_nearest_courier(self, coordinates: List[float], search_radius: float):
        query = {
            "status": "FREE",
            "latest_location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": coordinates,  # Coordenadas [longitude, latitude]
                    },
                    "$maxDistance": search_radius,  # Raio de busca em metros
                }
            },
        }
        couriers = list(mongo.orders.find(query))

        if couriers:
            return couriers
        return []
