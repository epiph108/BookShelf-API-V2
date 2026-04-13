# BookShelf API

A REST API built with FastAPI to manage a book collection with full CRUD operations, Pydantic validation, and proper error handling.

![Demo](Images/screenshot.png)

## Run it locally

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Swagger UI → `http://127.0.0.1:8000/docs`

## What you can do

- Get all books
- Get a book by ID
- Filter books by rating and published date
- Add a new book
- Update an existing book
- Delete a book

## Stack

- Python
- FastAPI
- Pydantic
