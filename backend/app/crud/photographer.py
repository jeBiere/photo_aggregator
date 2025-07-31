from sqlalchemy.orm import Session
from sqlalchemy import  func, case
from typing import List, Optional
from models.photographer import Photographer
from models.specialization import PhotographerSpecialization, SpecializationTypeEnum
from models.order import Order
from models.reviews import Review
from models.portfolio_item import PortfolioItem
from enum import Enum
from decimal import Decimal
from schemas.photographer import PhotographerCreate, PhotographerUpdate
from schemas.order import OrderInDB

def get_photographer(db: Session, photographer_id: int):
    return db.query(Photographer).filter(Photographer.photographer_id == photographer_id).first()

def get_photographers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Photographer).offset(skip).limit(limit).all()

def create_photographer(db: Session, photographer: PhotographerCreate):
    db_photographer = Photographer(**photographer.dict())
    db.add(db_photographer)
    db.commit()
    db.refresh(db_photographer)
    return db_photographer

def update_photographer(db: Session, photographer_id: int, updates: PhotographerUpdate):
    db_photographer = db.query(Photographer).filter(Photographer.photographer_id == photographer_id).first()
    if db_photographer:
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(db_photographer, field, value)
        db.commit()
        db.refresh(db_photographer)
    return db_photographer

def delete_photographer(db: Session, photographer_id: int):
    db_photographer = db.query(Photographer).filter(Photographer.photographer_id == photographer_id).first()
    if db_photographer:
        db.delete(db_photographer)
        db.commit()
    return db_photographer

def get_filtered_photographers(
    db: Session,
    city: Optional[str] = None,
    specializations: Optional[List[SpecializationTypeEnum]] = None,
    max_price: Optional[float] = None
) -> List[Photographer]:
    query = db.query(Photographer)
    
    if city:
        query = query.filter(Photographer.city == city) 
    
    if specializations:
        query = (
            query.join(PhotographerSpecialization)
            .filter(PhotographerSpecialization.specialization.in_(specializations))
            .distinct() 
        )
    
    # Фильтр по цене
    if max_price is not None:
        query = query.filter(Photographer.price_per_hour <= max_price)
    
    return query.all()

def get_sorted_by_relevance(
    db: Session,
    photographers: List[Photographer],
    rating_weight: float = 0.4,
    orders_weight: float = 0.3,
    reviews_weight: float = 0.15,
    experience_weight: float = 0.15,
) -> List[Photographer]:
    if not photographers:
        return []

    photographer_ids = [p.photographer_id for p in photographers]

    rating_weight_dec = Decimal(str(rating_weight))
    orders_weight_dec = Decimal(str(orders_weight))
    reviews_weight_dec = Decimal(str(reviews_weight))
    experience_weight_dec = Decimal(str(experience_weight))

    metrics = db.query(
        Photographer.photographer_id,
        func.count(
            case(
                (Order.status == 'completed', Order.order_id),
                else_=None
            )
        ).label('completed_orders'),
        func.count(Review.review_id).label('reviews_count')
    ).outerjoin(
        Order, Order.photographer_id == Photographer.photographer_id
    ).outerjoin(
        Review, Review.photographer_id == Photographer.photographer_id
    ).filter(
        Photographer.photographer_id.in_(photographer_ids)
    ).group_by(
        Photographer.photographer_id
    ).all()

    metrics_dict = {
        m.photographer_id: {
            'completed_orders': m.completed_orders,
            'reviews_count': m.reviews_count
        } for m in metrics
    }

    return sorted(
        photographers,
        key=lambda p: (
            Decimal(p.rating) * rating_weight_dec +
            Decimal(metrics_dict.get(p.photographer_id, {}).get('completed_orders', 0)) * orders_weight_dec +
            Decimal(metrics_dict.get(p.photographer_id, {}).get('reviews_count', 0)) * reviews_weight_dec +
            Decimal(p.experience_years or 0) * experience_weight_dec
        ),
        reverse=True
    )

def get_photographer_specializations(
    db: Session, 
    photographer_id: int
) -> List[SpecializationTypeEnum]:
    specializations = db.query(
        PhotographerSpecialization.specialization
    ).filter(
        PhotographerSpecialization.photographer_id == photographer_id
    ).all()
    
    return [s.specialization for s in specializations]

def get_photographer_reviews(
    db: Session, 
    photographer_id: int
):
     return db.query(Review).filter(
        Review.photographer_id == photographer_id
    ).all()

def get_photographer_portfolio(
    db: Session, 
    photographer_id: int
):
    return db.query(PortfolioItem).filter(
        PortfolioItem.photographer_id == photographer_id
    ).all()

def get_photographer_orders(db: Session, photographer_id: int, skip: int = 0, limit: int = 100) -> List[OrderInDB]:
    db_orders = db.query(Order)\
        .filter(Order.photographer_id == photographer_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return [OrderInDB.from_orm(order) for order in db_orders]

def get_photographer_by_user_id(db: Session, user_id: int):
    return db.query(Photographer).filter(Photographer.user_id == user_id).first()

