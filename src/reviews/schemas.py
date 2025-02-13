from pydantic import BaseModel
from sqlmodel import Field
from uuid import UUID
from typing import Optional
from datetime import datetime


class ReviewModel(BaseModel):
    uid: UUID
    rating: int = Field(lt=5)
    review_text: str 
    user_uid: Optional[UUID] 
    book_uid: Optional[UUID] 
    created_at:datetime 
    updated_at:datetime 


class ReviewCreateModel(BaseModel):
    rating: int = Field(lt=5)
    review_text: str 