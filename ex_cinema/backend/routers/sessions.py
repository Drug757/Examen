"""Роутер СЕАНСОВ — ЗАДАНИЕ.

═══════════════════════════════════════════════════════════════
ЗАДАНИЕ: реализуй 3 эндпоинта для управления сеансами

Модель данных сеанса:
{
    "id": 1,
    "movie_id": 1,        # привязка к фильму (должен существовать!)
    "time": "18:00",      # время сеанса
    "price": 450,         # цена билета (> 0)
    "seats": 50           # кол-во мест (> 0)
}

Начальные данные (скопируй в db):
[
    {"id": 1, "movie_id": 1, "time": "18:00", "price": 450, "seats": 50},
    {"id": 2, "movie_id": 1, "time": "21:00", "price": 550, "seats": 30},
    {"id": 3, "movie_id": 2, "time": "19:30", "price": 400, "seats": 60},
]

Что нужно реализовать:

1. GET /sessions/?movie_id=<int>  (необязательный query-параметр)
   - Без параметра → вернуть все сеансы
   - С movie_id → только сеансы этого фильма

2. POST /sessions/  (принимает SessionIn)
   - SessionIn: movie_id (int), time (str), price (int), seats (int)
   - ВАЖНО: проверь что фильм с movie_id существует!
   - price > 0, seats > 0, time не пустой
   - Верни созданный сеанс, status_code=201

3. DELETE /sessions/{session_id}  (status_code=204)
   - Удалить сеанс по id
   - Если не найден → 404

═══════════════════════════════════════════════════════════════
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from routers.movies import db as movies_db

router = APIRouter(prefix="/sessions", tags=["sessions"])

db: list[dict] = [
    {"id": 1, "movie_id": 1, "time": "18:00", "price": 450, "seats": 50},
    {"id": 2, "movie_id": 1, "time": "21:00", "price": 550, "seats": 30},
    {"id": 3, "movie_id": 2, "time": "19:30", "price": 400, "seats": 60},
]
next_id = 4


class SessionIn(BaseModel):
    movie_id: int
    time: str
    price: int
    seats: int


@router.get("/")
def get_sessions(movie_id: int | None = Query(None)):
    if movie_id is not None:
        return [s for s in db if s["movie_id"] == movie_id]
    return db


@router.get("/{session_id}")
def get_session(session_id: int):
    for s in db:
        if s["id"] == session_id:
            return s
    raise HTTPException(404, "Сеанс не найден")


@router.post("/", status_code=201)
def add_session(body: SessionIn):
    global next_id

    movie_exists = any(m["id"] == body.movie_id for m in movies_db)
    if not movie_exists:
        raise HTTPException(404, "Фильм не найден")

    if not body.time.strip():
        raise HTTPException(400, "Время не может быть пустым")
    if body.price <= 0:
        raise HTTPException(400, "Цена должна быть больше 0")
    if body.seats <= 0:
        raise HTTPException(400, "Количество мест должно быть больше 0")
    
    session = {
        "id": next_id,
        "movie_id": body.movie_id,
        "time": body.time.strip(),
        "price": body.price,
        "seats": body.seats,
    }
    db.append(session)
    next_id += 1
    return session


@router.delete("/{session_id}", status_code=204)
def delete_session(session_id: int):
    global db
    before = len(db)
    db = [s for s in db if s["id"] != session_id]
    if len(db) == before:
        raise HTTPException(404, "Сеанс не найден")