# models/__init__.py

from .base import Base
from .user import User, UserRole
from .photographer import Photographer
from .order import Order, OrderStatusEnum
from .reviews import Review
from .studio import PhotoStudio
from .specialization import PhotographerSpecialization, SpecializationTypeEnum
from .portfolio_photo import PortfolioPhoto
from .portfolio_item import PortfolioItem
from .schedule import WorkingHoursTemplate, BlockedSlot
from .studio_photo import StudioPhoto

# Здесь можно опционально собрать все модели в список (например, если понадобится):
ALL_MODELS = [
    User,
    Photographer,
    Order,
    Review,
    PhotoStudio,
    PhotographerSpecialization,
    PortfolioPhoto,
    PortfolioItem,
    WorkingHoursTemplate,
    BlockedSlot,
    StudioPhoto
    
]
