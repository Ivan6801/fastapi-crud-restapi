from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb+srv://hal308366:us8crCyC0sLhkbjC@fastapi.bwuhafu.mongodb.net/"
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.wms
movies_collection = db.get_collection("movies")
