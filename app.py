from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from bson import ObjectId
from database import db
from models import Movie

app = FastAPI()
app.title = "Mi aplicación con FastAPI"
app.version = "0.0.1"

# Helper function to serialize ObjectId


def serialize_movie(movie):
    movie["_id"] = str(movie["_id"])  # Convert ObjectId to string
    return movie


@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')


@app.get("/movies/")
async def get_movies():
    try:
        movies = await db.movies.find().to_list(length=100)
        return [serialize_movie(movie) for movie in movies]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/movies/")
async def create_movie(movie: Movie):
    try:
        new_movie = await db.movies.insert_one(movie.dict())
        return {"id": str(new_movie.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/movies/{id}', tags=['movies'])
async def get_movie(id: str):
    try:
        movie = await db.movies.find_one({"_id": ObjectId(id)})
        if movie:
            return serialize_movie(movie)
        raise HTTPException(status_code=404, detail="Movie not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put('/movies/{id}', tags=['movies'])
async def update_movie(id: str, movie: Movie):
    try:
        result = await db.movies.update_one({"_id": ObjectId(id)}, {"$set": movie.dict()})
        if result.modified_count:
            return {**movie.dict(), "id": id}
        raise HTTPException(status_code=404, detail="Movie not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete('/movies/{id}', tags=['movies'])
async def delete_movie(id: str):
    try:
        result = await db.movies.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return {"message": "Movie deleted"}
        raise HTTPException(status_code=404, detail="Movie not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
