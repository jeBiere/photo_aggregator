
from routers import order_router, phototgrapher_router, user_router, portfolio_item, reviews, schedule, specialization, studio_router, portfolio_photo
from crud import order
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from utils.schedular import start_scheduler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI()

@app.on_event("startup")
def on_startup():
    start_scheduler()  # Запускаем планировщик при старте

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать конкретные домены
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Подключение обработчиков (handlers)
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(studio_router.router, prefix="/studios", tags=["studios"])
app.include_router(phototgrapher_router.router, prefix="/photographers", tags=["photographers"])
app.include_router(order_router.router, prefix="/orders", tags=["orders"])
app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
app.include_router(portfolio_item.router, prefix="/portfolio_items", tags=["portfolio_items"])
app.include_router(schedule.router, prefix="/schedules", tags=["schedules"])
app.include_router(specialization.router, prefix="/specializations", tags=["specializations"])
app.include_router(portfolio_photo.router, prefix="/portfolio_photos", tags=["portfolio_photos"])





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

Instrumentator().instrument(app).expose(app)