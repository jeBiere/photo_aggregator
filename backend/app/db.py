import os
import psycopg2
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Подключение к MongoDB
mongo_host = os.getenv("MONGO_HOST", "mongodb")
mongo_port = int(os.getenv("MONGO_PORT", 27017))
mongo_db = os.getenv("MONGO_INITDB_DATABASE", "photo_aggr")
client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}/")
db = client[mongo_db]

photographers_collection = db["photographers"]
clients_collection = db["clients"]
orders_collection = db["orders"]
services_collection = db["services"]
requests_collection = db["requests"]

# Подключение к PostgreSQL
postgres_host = os.getenv("POSTGRES_HOST", "postgres-1")
postgres_user = os.getenv("POSTGRES_USER", "postgres")
postgres_password = os.getenv("POSTGRES_PASSWORD", "postgres")
postgres_db = os.getenv("POSTGRES_DB", "photo_aggr")

SQLALCHEMY_DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"


# Создаем объект для работы с базой данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Создаем функцию для получения сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


