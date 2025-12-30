from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date

ALLOWED_CURRENCIES = {"USD"}  # Permitted coins

class BankTransactionCreate(BaseModel):
    external_id: str = Field(..., example="TXN-001")
    amount: float = Field(..., gt=0, example=150.75)
    currency: str = Field(..., example="USD")
    transaction_date: Optional[date] = Field(None, example="2025-01-15")
    description: Optional[str] = Field(None, example="Payment received")

    @validator("currency")
    def validate_currency(cls, v):
        if v not in ALLOWED_CURRENCIES:
            raise ValueError(f"Currency must be one of: {', '.join(ALLOWED_CURRENCIES)}")
        return v

    @validator("amount")
    def validate_vendor_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("this value must be a positive number")
        return v
