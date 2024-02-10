from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field


class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_data: str = None


class ContactVaccinatedModel(BaseModel):
    vaccinated: bool = False


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_data: str = None
