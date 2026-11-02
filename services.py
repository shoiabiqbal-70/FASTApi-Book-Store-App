
from models import Books
from sqlalchemy.orm import Session
from schemas import BookCreate


# CREATE: Add a new book
def create_book(db: Session, data: BookCreate):
    book_instance = Books(**data.model_dump())

    db.add(book_instance)
    db.commit()
    db.refresh(book_instance)

    return book_instance


# READ: Retrieve all books
def get_books(db: Session):
    return db.query(Books).all()


# READ: Retrieve a single book
def get_book(db: Session, book_id: int):
    return db.query(Books).filter(Books.id == book_id).first()


# UPDATE: Update an existing book
def update_book(db: Session, book: BookCreate, book_id: int):
    book_queryset = (
        db.query(Books).filter(Books.id == book_id).first()
    )

    if book_queryset:
        for key, value in book.model_dump().items():
            setattr(book_queryset, key, value)

        db.commit()
        db.refresh(book_queryset)

        return book_queryset

    return None


# DELETE: Delete an existing book
def delete_book(db: Session, book_id: int):
    book_queryset = (
        db.query(Books).filter(Books.id == book_id).first()
    )

    if book_queryset:
        db.delete(book_queryset)
        db.commit()

        return {"message": "Book deleted successfully"}

    return None