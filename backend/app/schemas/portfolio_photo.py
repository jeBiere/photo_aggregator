# schemas/portfolio_photo.py
from pydantic import BaseModel

class PortfolioPhotoInDB(BaseModel):
    photo_id: int
    item_id: int
    file_path: str

    class Config:
        orm_mode = True
