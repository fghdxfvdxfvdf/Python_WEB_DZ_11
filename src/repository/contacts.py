from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
import sys

sys.path.append(str(BASE_DIR))


from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactCreate, ContactVaccinatedModel


async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def create(body: ContactCreate, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactCreate, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birth_date = body.birth_date
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def set_vaccinated(contact_id: int, body: ContactVaccinatedModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.vaccinated = body.vaccinated
        db.commit()
    return contact
