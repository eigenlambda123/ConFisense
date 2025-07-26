from fastapi import FastAPI
from app.db.base import init_db
from app.api.routes import (
    simulate_emergency,
    simulate_budgeting,
    simulate_debt_management,
    simulate_investing,
    simulate_education_fund
)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(simulate_emergency.router)
app.include_router(simulate_budgeting.router)
app.include_router(simulate_debt_management.router)
app.include_router(simulate_investing.router)
app.include_router(simulate_education_fund.router)
