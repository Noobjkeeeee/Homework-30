from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text

from .database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    views = Column(Integer, default=0)
    cooking_time = Column(Integer)
    ingredients = Column(Text)
    description = Column(Text)

    def __repr__(self):
        return f"<Recipe(title={self.title}, views={self.views}, cooking_time={self.cooking_time})>"


class RecipeCreate(BaseModel):
    title: str
    cooking_time: int
    ingredients: str
    description: str


class RecipeResponse(RecipeCreate):
    id: int

    class Config:
        orm_mode = True
