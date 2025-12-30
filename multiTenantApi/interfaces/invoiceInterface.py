from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional

# Allowed values
ALLOWED_CURRENCIES = {"USD"}  # Permitted coins
ALLOWED_STATUS = {"open", "paid", "cancelled"}  # Validate status

class InvoiceCreate(BaseModel):
    vendor_id: Optional[int] = Field(None, example=10)
    invoice_number: Optional[str] = Field("INV-001", example="INV-001")
    amount: float = Field(..., gt=0, example=150.75)
    currency: str = Field("USD", example="USD")
    invoice_date: Optional[date] = Field(None, example="2025-01-15")
    description: Optional[str] = Field(None, example="Monthly service")
    status: str = Field("open", example="open")

    @validator("currency")
    def validate_currency(cls, v):
        if v not in ALLOWED_CURRENCIES:
            
            return {"error": True, "message": f"The coin is a USD: {', '.join(ALLOWED_CURRENCIES)}"}

    @validator("status")
    def validate_status(cls, v):
        if v not in ALLOWED_STATUS:
            raise ValueError(f"Invalid status must be: {', '.join(ALLOWED_STATUS)}")
        return v

    @validator("vendor_id")
    def validate_vendor_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("This value must be a positive number")
        return v
