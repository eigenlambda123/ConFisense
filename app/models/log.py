from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON

class SimulationLog(SQLModel, table=True):
    """
    Model for logging simulation inputs and outputs
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    scenario: str
    input_data: JSON
    output_data: JSON
    created_at: datetime = Field(default_factory=datetime.utcnow)