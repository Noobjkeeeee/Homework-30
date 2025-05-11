from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, init_db
from .models import Recipe, RecipeCreate, RecipeResponse

app = FastAPI()

init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/recipes", response_model=list[RecipeResponse])
def read_recipes(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    """
    Получить список всех рецептов.

    - **skip**: Количество пропускаемых записей (для пагинации).
    - **limit**: Максимальное количество возвращаемых записей.

    Рецепты сортируются по количеству просмотров и времени приготовления.
    """
    return (
        db.query(Recipe)
        .order_by(Recipe.views.desc(), Recipe.cooking_time)
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.get("/recipes/{recipe_id}", response_model=RecipeResponse)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Получить детальную информацию о конкретном рецепте по его ID.

    - **recipe_id**: ID рецепта.

    Возвращает информацию о названии блюда,
    времени приготовления,
    списке ингредиентов и текстовом описании.
    """
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if recipe is None:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    return recipe


@app.post("/recipes", response_model=RecipeResponse)
def create_recipe(recipe_create: RecipeCreate, db: Session = Depends(get_db)):
    """
    Создать новый рецепт.

    - **recipe**: Объект нового рецепта с полями title,
      cooking_time, ingredients и description.

    Возвращает созданный рецепт с его ID.
    """

    recipe = Recipe(**recipe_create.dict())

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return recipe
