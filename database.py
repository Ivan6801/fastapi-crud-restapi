from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

MONGO_DETAILS = "mongodb+srv://hal308366:us8crCyC0sLhkbjC@fastapi.bwuhafu.mongodb.net/"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.wms
post_collection = database.get_collection("posts")


async def create_post(post_data):
    result = await post_collection.insert_one(post_data)
    return str(result.inserted_id)


async def get_post(post_id):
    post = await post_collection.find_one({"_id": ObjectId(post_id)})
    return post


def serialize_document(doc):
    if doc is not None:
        doc['_id'] = str(doc['_id'])
    return doc
