db = db.getSiblingDB('delivery'); 
db.orders.createIndex({ latest_location: "2dsphere" });
