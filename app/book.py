from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # creates books.db automatically

def seed_data():
    db = SessionLocal()
    if db.query(models.Book).count() == 0:  # only runs if db is empty
        starter_books = [
            models.Book(title="The Hidden Reality", author="Brian Greene", description="Parallel universes and the deep laws of the cosmos", rating=5),
            models.Book(title="A Brief History of Time", author="Stephen Hawking", description="The origin and fate of the universe", rating=5),
            models.Book(title="Sapiens", author="Yuval Noah Harari", description="A brief history of humankind", rating=4),
            models.Book(title="Flatland", author="Edwin A. Abbott", description="A romance of many dimensions", rating=3),
            models.Book(title="SPQR", author="Mary Beard", description="A history of ancient Rome", rating=4),
        ]
        db.add_all(starter_books)
        db.commit()
    db.close()

seed_data()
class BookRequest(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/books")
async def read_all_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@app.get("/books/{book_id}")
async def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/create-book")
async def create_book(book_request: BookRequest, db: Session = Depends(get_db)):
    new_book = models.Book(**book_request.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.put("/books/{book_id}")
async def update_book(book_id: int, book_request: BookRequest, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = book_request.title
    book.author = book_request.author
    book.description = book_request.description
    book.rating = book_request.rating
    db.commit()
    return book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()