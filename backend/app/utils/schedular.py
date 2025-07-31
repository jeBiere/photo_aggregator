from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from crud import order  # Импортируем функцию для удаления заказов
from sqlalchemy.orm import Session
from db import get_db  # Импортируем функцию для получения сессии

# Функция для удаления старых отменённых заказов
def scheduled_delete_old_orders():
    db: Session = next(get_db())  # Получаем сессию для работы с БД
    order.delete_old_cancelled_orders(db)  # Удаляем старые заказы

# Настройка планировщика задач
def start_scheduler():
    scheduler = BackgroundScheduler()
    # Запуск задачи каждый день (каждые 24 часа)
    scheduler.add_job(scheduled_delete_old_orders, 'interval', days=1)
    scheduler.start()
