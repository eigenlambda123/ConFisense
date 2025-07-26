from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON
from datetime import datetime


class SimulationLog(SQLModel, table=True):
    """
    Model for logging simulation inputs and outputs
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    scenario: str
    input_data: dict = Field(sa_column=Column(JSON))
    output_data: dict = Field(sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)