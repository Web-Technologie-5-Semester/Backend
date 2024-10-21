# from fastapi import FastAPI
# from ..models.books import Book
# from ..db.books_repository import BooksRepository, Singleton, get_db
# from fastapi import APIRouter, Depends, Query
# from sqlalchemy.orm import Session, sessionmaker


# router = APIRouter()

# rep = BooksRepository(engine)


# @router.get("/books")
# async def get_books(db: Session = Depends(get_db)):
#     rep.get_all()
#     return Book

# @router.get("/books/{book_isbn}")
# async def get_book_by_isbn(book_isbn: int, db: Session = Depends(get_db)):
#     rep.get_by_isbn(book_isbn)
#     return {"book_isbn": book_isbn}

# @router.delete("/books")
# async def delete_book_by_isbn(book_isbn: int, db: Session = Depends(get_db)):
#     rep.delete_by_isbn(book_isbn)
#     return {"book:", book_isbn, " deleted"}

# @router.post("/books")
# async def create_book(book: Book, db: Session = Depends(get_db)):
#     new_book = book
#     db.add(new_book)
#     db.commit()
#     db.refresh(new_book)
#     return new_book

# @router.put("/books")
# async def update_book(book: Book, db: Session = Depends(get_db)):
#     new_book = book
#     rep.update(new_book)
#     db.add(new_book)
#     db.commit()
#     db.refresh(new_book)
#     return new_book

