from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
import sys

sys.path.append(str(BASE_DIR))



from datetime import date, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact
from src.repository import contacts as repository_contacts
from src.schemas import ContactCreate, ContactResponse, ContactVaccinatedModel

router = APIRouter(prefix="/contacts", tags=['contacts'])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactCreate, db: Session = Depends(get_db)):
    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_cat(body: ContactCreate, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.patch("/{contact_id}/vaccinated", response_model=ContactResponse)
async def vaccinated_contact(body: ContactVaccinatedModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.set_vaccinated(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/contacts/birthdays", response_model=List[ContactResponse])
def upcoming_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    next_week = today + timedelta(days=7)
    birthdays = db.query(Contact).filter(
        (today <= Contact.birth_date) & (Contact.birth_date <= next_week)
    ).all()
    db.close()
    return birthdays


@router.get("/search-contact/", response_model=List[ContactResponse])
def search_contact(search_query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    contacts = repository_contacts.search_contacts(db, search_query)
    return [{"id": contact.id, "first_name": contact.first_name, "last_name": contact.last_name, 
            "email": contact.email, "phone_number": contact.phone_number, "birth_date": contact.birth_date, 
            "additional_data": contact.additional_data} for contact in contacts]

