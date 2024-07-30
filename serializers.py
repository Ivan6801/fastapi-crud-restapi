from bson import ObjectId
from fastapi.encoders import jsonable_encoder


def objectid_encoder(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(
        f"Object of type {obj.__class__.__name__} is not JSON serializable")


def custom_jsonable_encoder(obj):
    return jsonable_encoder(obj, custom_encoder={ObjectId: objectid_encoder})
