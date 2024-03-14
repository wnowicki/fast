from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

# from .dependencies import get_query_token, get_token_header
from . import dto, repositories
from .database import SessionLocal
# from .internal import admin
# from .routers import items, users

# from .database import Base, engine
# import app.models
# Base.metadata.create_all(engine)

app = FastAPI(dependencies=[])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=dto.User)
def create_user(user: dto.UserCreate, db: Session = Depends(get_db)):
    db_user = repositories.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return repositories.create_user(db=db, user=user)


@app.get("/users/", response_model=list[dto.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = repositories.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=dto.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = repositories.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=dto.Item)
def create_item_for_user(
    user_id: int, item: dto.ItemCreate, db: Session = Depends(get_db)
):
    return repositories.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[dto.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = repositories.get_items(db, skip=skip, limit=limit)
    return items
