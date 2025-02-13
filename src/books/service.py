# src/books/service.py
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, BookUpdateModel
from sqlmodel import select, desc
from src.db.models import Book
from datetime import datetime

class BookService:
    async def get_all_books(self, session:AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_user_books(self, user_uid:str, session:AsyncSession):
        statement = select(Book).where(Book.user_uid == user_uid).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid: str, session:AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    async def create_book(self, book_data: BookCreateModel, user_uid: str ,session:AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict) # Unpack the 'book_data_dict' to create a 'Book' object with the provided request body data
        new_book.published_date = datetime.strptime(book_data_dict['published_date'], "%Y-%m-%d")
        new_book.user_uid = user_uid
        session.add(new_book)
        await session.commit()

        return new_book

    async def update_book(self, book_uid: str, update_data: BookUpdateModel, session:AsyncSession):
        book_to_update = await self.get_book(book_uid, session)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump()
            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)
            
            # Update the timestamp
            book_to_update.updated_at = datetime.now()

            await session.commit()
            await session.refresh(book_to_update)  # Refresh to get the updated state
            return book_to_update
        else:
            return None


    async def delete_book(self, book_uid: str, session:AsyncSession):
        book_to_delete = await self.get_book(book_uid, session)

        if book_to_delete is not None:
            await session.delete(book_to_delete)

            await session.commit()
            return True # Indicate successful deletion
        return None # Indicate book not found




