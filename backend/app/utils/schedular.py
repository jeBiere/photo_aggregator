from apscheduler.schedulers.background import BackgroundScheduler
from crud import order 
from sqlalchemy.orm import Session
from db import get_db 

def scheduled_delete_old_orders():
    db: Session = next(get_db()) 
    order.delete_old_cancelled_orders(db) 

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_delete_old_orders, 'interval', days=1)
    scheduler.start()
