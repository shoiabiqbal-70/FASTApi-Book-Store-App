
"""
FastAPI entry point for the Bookstore app.

Defines HTTP endpoints for CRUD operations on books.
Run with: uvicorn main:app --reload
"""

from fastapi import FastAPI, Depends, HTTPException
import services
import schemas
from db import get_db, create_table
from sqlalchemy.orm import Session
import models  # Registers database models


# Create database tables
create_table()

# Initialize FastAPI
app = FastAPI()


# GET: Retrieve all books
@app.get("/books/", response_model=list[schemas.Book])
async def get_all_books(db: Session = Depends(get_db)):
    return services.get_books(db)


# GET: Retrieve a single book
@app.get("/books/{id}", response_model=schemas.Book)
async def get_book_by_id(id: int, db: Session = Depends(get_db)):
    book_queryset = services.get_book(db, id)

    if book_queryset:
        return book_queryset

    raise HTTPException(
        status_code=404,
        detail="Invalid Book ID Provided or Book ID does not exist"
    )


# POST: Create a new book
@app.post("/books/", response_model=schemas.Book)
async def create_new_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    return services.create_book(db, book)


# PUT: Update an existing book
@app.put("/books/{id}", response_model=schemas.Book)
async def update_book(
    book: schemas.BookCreate,
    id: int,
    db: Session = Depends(get_db)
):
    db_update = services.update_book(db, book, id)

    if not db_update:
        raise HTTPException(
            status_code=404,
            detail="Book Not Found"
        )

    return db_update


# DELETE: Delete a book
@app.delete("/books/{id}")
async def delete_book(id: int, db: Session = Depends(get_db)):
    delete_entry = services.delete_book(db, id)

    if delete_entry:
        return delete_entry

    raise HTTPException(
        status_code=404,
        detail="Book Not Found"
    )