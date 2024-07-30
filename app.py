from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime
from bson import ObjectId
from database import post_collection, create_post, get_post, serialize_document
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

posts = []

# Post model


class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: Optional[bool] = False
    imagen: Optional[str] = None


@app.get('/')
def read_root():
    return {"welcome": "Welcome to my API"}


@app.get('/posts')
async def get_posts():
    posts = []
    async for post in post_collection.find():
        posts.append(serialize_document(post))
    return posts


@app.post('/posts')
async def save_post(post: Post):
    post_data = jsonable_encoder(post)
    new_post_id = await create_post(post_data)
    created_post = await get_post(new_post_id)
    return JSONResponse(status_code=201, content=created_post)


@app.get('/posts/{post_id}')
async def get_post(post_id: str):
    post = await post_collection.find_one({"_id": ObjectId(post_id)})
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.delete('/posts/{post_id}')
async def delete_post(post_id: str):
    delete_result = await post_collection.delete_one({"_id": ObjectId(post_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Post has been deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")


@app.put('/posts/{post_id}')
async def update_post(post_id: str, updated_post: Post):
    update_result = await post_collection.update_one(
        {"_id": ObjectId(post_id)}, {"$set": updated_post.dict()}
    )
    if update_result.modified_count == 1:
        updated_post = await post_collection.find_one({"_id": ObjectId(post_id)})
        return updated_post
    raise HTTPException(status_code=404, detail="Post not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
