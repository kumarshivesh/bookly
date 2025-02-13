from src.db.models import Review
from src.auth.service import UserService
from src.books.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import status
from .schemas import ReviewCreateModel
from fastapi.exceptions import HTTPException
import logging
from sqlmodel import select, desc

book_service = BookService()
user_service = UserService()

class ReviewService:
    async def add_review_to_book(
        self, 
        user_email: str, 
        book_uid: str, 
        review_data: ReviewCreateModel, 
        session: AsyncSession
    ):
        try:
            book = await book_service.get_book(book_uid=book_uid, session=session)
            user = await user_service.get_user_by_email(email=user_email, session=session)
            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Book not found."
                )
            new_review.book = book
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )
            new_review.user = user

            session.add(new_review)
            await session.commit()
            return new_review
        except Exception as e:
            logging.exception(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Oops.. Something went wrong"
            ) 
        
    async def get_review(self, review_uid: str, session: AsyncSession):
        statement = select(Review).where(Review.uid == review_uid)

        result = await session.exec(statement)
        review = result.first()
        #print(review)
        return review if review is not None else None

    async def get_all_reviews(self, session: AsyncSession):
        statement = select(Review).order_by(desc(Review.created_at))

        result = await session.exec(statement)

        return result.all()

    async def delete_review_to_from_book(self, review_uid: str, session: AsyncSession):

        review = await self.get_review(review_uid, session)

        if review is not None:
            await session.delete(review)

            await session.commit()
            return True # Indicate successful deletion
        return None # Indicate book not found