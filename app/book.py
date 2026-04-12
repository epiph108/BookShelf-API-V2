from fastapi import Body,FastAPI
from pydantic import BaseModel
app = FastAPI()

class Book:
  id : int
  title : str
  author : str 
  description : str
  rating : int

  def __init__(self,id,title,author,description,rating):
    self.id = id
    self.title = title
    self.author = author
    self.description = description
    self.rating = rating


class BookRequest(BaseModel):
  id : int
  title : str
  author : str 
  description : str
  rating : int


BOOKS = [
        Book(1, "The Hidden Reality", "Brian Greene", "Parallel universes and the deep laws of the cosmos", 5),
        Book(2, "A Brief History of Time", "Stephen Hawking", "The origin and fate of the universe", 5),
        Book(3, "Sapiens", "Yuval Noah Harari", "A brief history of humankind", 4),
        Book(4, "Gödel, Escher, Bach", "Douglas Hofstadter", "A metaphorical fugue on minds and machines", 5),
        Book(5, "Flatland", "Edwin A. Abbott", "A romance of many dimensions", 3),
        Book(6, "The Name of the Rose", "Umberto Eco", "A medieval mystery set in an Italian monastery", 4),
        Book(7, "The Code Book", "Simon Singh", "The science of secrecy from ancient Egypt to quantum cryptography", 4),
        Book(8, "SPQR", "Mary Beard", "A history of ancient Rome", 4),
        Book(9, "The Drunkard's Walk", "Leonard Mlodinow", "How randomness rules our lives", 3),
        Book(10, "Seven Brief Lessons on Physics", "Carlo Rovelli", "Modern physics for curious readers", 5)
]

@app.get("/books")
async def read_all_books():
  return BOOKS 

@app.post("/create-book")
async def create_book(book_request: BookRequest):
  new_book = Book(**book_request.model_dump())
  BOOKS.append(book_request)