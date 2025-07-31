# schemas/portfolio_photo.py
from pydantic import BaseModel

class PortfolioPhotoInDB(BaseModel):
    studio_id: int
    photo_id: int
    file_path: str

    class Config:
        orm_mode = True
