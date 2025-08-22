from fastapi import FastAPI
from app.db.base import init_db
from app.api.routes import (
    simulate_budget_optimization,
    simulate_budgeting,
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

app.include_router(simulate_budget_optimization.router, tags=["Budget Optimization"])