from fastapi import FastAPI
from app.db.base import init_db
from app.api.routes import (
    simulate_emergency_fund,
    simulate_budgeting,
    simulate_debt_management,
    simulate_investing,
    simulate_education_fund,
    simulate_major_purchase
)

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(simulate_budgeting.router, tags=["Budgeting Simulation"])
