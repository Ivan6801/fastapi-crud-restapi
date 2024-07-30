from pydantic import BaseModel, Field
from bson import ObjectId


class Movie(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
