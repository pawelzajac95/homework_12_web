from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta
from src.database.models import User
from src.database.models import Contact as SQLAlchemyContact
from src.schemas import ContactCreate, UserModel
from typing import List




async def get_contact(db: Session, user: User, contact_id: int) -> SQLAlchemyContact:
    return db.query(SQLAlchemyContact).filter(and_(ContactCreate.id == contact_id, SQLAlchemyContact.user_id == user.id)).first()

async def get_contacts(db: Session, user: User, search_query: str = None) -> List[SQLAlchemyContact]:
    query = db.query(SQLAlchemyContact).filter(SQLAlchemyContact.user_id == user.id)
    
    if search_query:
        search_filter = or_(
            SQLAlchemyContact.first_name.ilike(f"%{search_query}%"),
            SQLAlchemyContact.last_name.ilike(f"%{search_query}%"),
            SQLAlchemyContact.email.ilike(f"%{search_query}%")
        )
        query = query.filter(search_filter)
    
    return query.all()

async def create_contact(db: Session, contact: ContactCreate, user: User) -> SQLAlchemyContact:
    db_contact = SQLAlchemyContact(first_name=contact.first_name, last_name=contact.last_name, email=contact.email, phone_number=contact.phone_number, birth_date=contact.birth_date, user=user)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

async def update_contact(db: Session, user: User, contact_id: int, contact: ContactCreate) -> SQLAlchemyContact | None:
    db_contact = await get_contact(db, contact_id, user.id)
    if not db_contact:
        return None
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

async def delete_contact(db: Session, user: User, contact_id: int) -> SQLAlchemyContact | None:
    db_contact = await get_contact(db, contact_id, user.id)
    if not db_contact:
        return None
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted successfully"}

async def get_contacts_upcoming_birthdays(db: Session) -> SQLAlchemyContact | None:
    today = datetime.today().date()
    end_date = today + timedelta(days=7)
    return db.query(SQLAlchemyContact).filter(
        (SQLAlchemyContact.birth_date >= today) & (SQLAlchemyContact.birth_date <= end_date)
    ).all()

