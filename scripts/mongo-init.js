db = db.getSiblingDB('delivery'); 
db.courier_locations.createIndex({ latest_location: "2dsphere" });
db.courier_locations.createIndex({ order_number: "text" });
