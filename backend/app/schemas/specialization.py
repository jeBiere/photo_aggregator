from pydantic import BaseModel
from enum import Enum

# Определяем Enum для специализаций фотографов
class SpecializationType(str, Enum):
    portrait = "portrait"
    wedding = "wedding"
    family = "family"
    children = "children"
    event = "event"
    fashion = "fashion"
    boudoir = "boudoir"
    sports = "sports"
    studio = "studio"
    on_location = "on_location"
    product = "product"
    love_story = "love_story"

# Схема для валидации специализаций фотографа
class PhotographerSpecializationBase(BaseModel):
    photographer_id: int
    specialization: SpecializationType

    class Config:
        orm_mode = True

# Схема для создания новой специализации фотографа
class PhotographerSpecializationCreate(PhotographerSpecializationBase):
    pass  # Можно добавить дополнительные поля для создания, если потребуется

# Схема для вывода данных (например, в ответах API)
class PhotographerSpecializationInDB(PhotographerSpecializationBase):
    pass  # Можно добавить дополнительные поля, если потребуется
