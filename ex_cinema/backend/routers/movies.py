from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/movies", tags=["movies"])

db: list[dict] = [
    {"id": 1, "title": "Интерстеллар",  "genre": "Фантастика", "year": 2014},
    {"id": 2, "title": "Начало",         "genre": "Триллер",    "year": 2010},
    {"id": 3, "title": "Довод",          "genre": "Фантастика", "year": 2020},
]
next_id = 4

class MovieIn(BaseModel):
    title: str
    genre: str
    year: int

@router.get("/")
def get_movies():
    return db

@router.get("/{movie_id}")
def get_movie(movie_id: int):
    for m in db:
        if m["id"] == movie_id:
            return m
    raise HTTPException(404, "Фильм не найден")


@router.post("/", status_code=201)
def add_movie(body: MovieIn):
    global next_id
    if not body.title.strip():
        raise HTTPException(400, "Название не может быть пустым")
    if body.year < 1900 or body.year > 2030:
        raise HTTPException(400, "Некорректный год")

    movie = {
        "id": next_id,
        "title": body.title.strip(),
        "genre": body.genre.strip(),
        "year": body.year,
    }
    db.append(movie)
    next_id += 1
    return movie


@router.delete("/{movie_id}", status_code=204)
def delete_movie(movie_id: int):
    global db
    before = len(db)
    db = [m for m in db if m["id"] != movie_id]
    if len(db) == before:
        raise HTTPException(404, "Фильм не найден")
