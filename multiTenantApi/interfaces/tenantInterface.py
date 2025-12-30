from pydantic import BaseModel, Field
from datetime import datetime


class TenantCreate(BaseModel):
    name: str = Field(..., example="Acme Corp")


class TenantResponse(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True
