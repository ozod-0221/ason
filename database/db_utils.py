
from .db import *
from .models import *
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from sqlalchemy import select, join,delete
from sqlalchemy.orm import joinedload
import pandas as pd
from sqlalchemy import desc



async def add_user(
    telegram_user_id: int,
    name: str = None,
    phone_number: str = None,
    role: RoleEnum = RoleEnum.USER
):
    async with async_session() as session:
        new_user = User(
            telegram_user_id=telegram_user_id,
            name=name,
            phone_number=phone_number,
            role=role
        )
        session.add(new_user)
        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()
async def user_exists(telegram_user_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_user_id == telegram_user_id)
        )
        user = result.scalar_one_or_none()
        return user is not None
async def get_event_by_referral_id(referral_id: str) -> Event | None:
    async with async_session() as session:
        result = await session.execute(
            select(Event).where(Event.events_referal_id == referral_id)
        )
        return result.scalar_one_or_none() 
async def  exist_event(referral_id: str) -> bool:
    async with async_session() as session:
        result = await session.execute(
            select(Event).where(Event.events_referal_id == referral_id)
        )
        event = result.scalar_one_or_none()
        return event is not None



async def add_event(name: str, referral_id: str,link:str) -> bool:
    async with async_session() as session:
        new_event = Event(name=name, events_referal_id=referral_id,link=link)
        session.add(new_event)
        try:
            await session.commit()
            return True
        except IntegrityError:
            await session.rollback()
            return False
async def get_participant_count_by_referral(referral_code: str) -> int:
    async with async_session() as session:
        result = await session.execute(
            select(func.count(EventParticipant.id))
            .join(Event, EventParticipant.event_id == Event.id)
            .where(Event.events_referal_id == referral_code)
        )
        return result.scalar() or 0
async def get_statistics():
    async with async_session() as session:
        result = await session.execute(select(Event))
        events = result.scalars().all()
        
        return events

async def user_exist_in_event(telegram_user_id: int, referral_code: str) -> bool:
    async with async_session() as session:
        # Avval referral_code bo'yicha eventni topamiz
        event = await get_event_by_referral_id(referral_code)
        if not event:
            return False
            
        # Endi userning shu eventda bor-yo'qligini tekshiramiz
        result = await session.execute(
            select(EventParticipant).where(
                EventParticipant.telegram_user_id == telegram_user_id,
                EventParticipant.event_id == event.id  # event_id orqali qidirish
            )
        )
        return result.scalar_one_or_none() is not None
async def add_event_participant(telegram_user_id: int, event_id: int, joined_at: datetime) -> bool:
    async with async_session() as session:
        new_participant = EventParticipant(
            telegram_user_id=telegram_user_id,
            event_id=event_id,
            joined_at=joined_at
        )
        session.add(new_participant)
        try:
            await session.commit()
            return True
        except IntegrityError as e:
            await session.rollback()
            print(f"IntegrityError: {e}")
            return False
        except Exception as e:
            await session.rollback()
            print(f"Unexpected error: {e}")
            return False
async def get_all_user_ids():
    async with async_session() as session:
        result = await session.execute(select(User.telegram_user_id))
        return result.scalars().all()
from sqlalchemy import select, join
from sqlalchemy.orm import joinedload
import pandas as pd
from datetime import datetime

async def get_event_participants_data(event_id: int):
    """
    Event ID bo'yicha barcha qatnashchilarni ma'lumotlarini olish
    """
    async with async_session() as session:
        # Event va User ma'lumotlarini birga olish uchun join qilamiz
        query = (
            select(
                User.telegram_user_id,
                User.name,
                User.phone_number,
                User.role,
                EventParticipant.joined_at,
                Event.name.label("event_name"),
                Event.events_referal_id
            )
            .select_from(
                join(EventParticipant, User, EventParticipant.telegram_user_id == User.telegram_user_id)
                .join(Event, EventParticipant.event_id == Event.id)
            )
            .where(EventParticipant.event_id == event_id)
        )
        
        result = await session.execute(query)
        participants = result.mappings().all()
        
        return participants

async def export_participants_to_excel(event_id: int, filename: str = None):
    """
    Qatnashchilarni Excel fayliga eksport qilish
    """
    participants = await get_event_participants_data(event_id)
    
    if not participants:
        return None  # Agar qatnashchilar bo'lmasa
    
    # Pandas DataFrame yaratish
    df = pd.DataFrame([dict(p) for p in participants])
    
    # Sana formatini o'zgartirish
    df['joined_at'] = df['joined_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Agar filename kiritilmagan bo'lsa, avtomatik yaratish
    if not filename:
        filename = f"event_{event_id}_participants_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    
    # Excel fayliga yozish
    df.to_excel(filename, index=False, engine='openpyxl')
    
    return filename
from sqlalchemy import update

async def update_user(
    telegram_user_id: int,
    name: str = None,
    phone_number: str = None,
    role: RoleEnum = None
):
    async with async_session() as session:
        # Yangilanish kerak bo'lgan maydonlarni to'plab olamiz
        update_data = {}
        if name is not None:
            update_data["name"] = name
        if phone_number is not None:
            update_data["phone_number"] = phone_number
        if role is not None:
            update_data["role"] = role
            
        # Agar yangilanish kerak bo'lgan maydonlar bo'lsa
        if update_data:
            await session.execute(
                update(User)
                .where(User.telegram_user_id == telegram_user_id)
                .values(**update_data)
            )
            await session.commit()
# database/db_utils.py



async def user_exist_in_event(telegram_user_id: int, event_id: int) -> bool:
    """Foydalanuvchi eventda borligini tekshirish"""
    async with async_session() as session:
        result = await session.execute(
            select(EventParticipant).where(
                EventParticipant.telegram_user_id == telegram_user_id,
                EventParticipant.event_id == event_id
            )
        )
        return result.scalar_one_or_none() is not None
async def get_active_event() -> Event | None:
    async with async_session() as session:
        result = await session.execute(
            select(Event).where(Event.is_active == True)
        )
        return result.scalar_one_or_none()
async def deactivate_event(event_id: int):
    async with async_session() as session:
        await session.execute(
            update(Event).where(Event.id == event_id).values(is_active=False)
        )
        await session.commit()
async def activate_event(event_id: int):
    async with async_session() as session:
        await session.execute(
            update(Event).where(Event.id == event_id).values(is_active=True)
        )
        await session.commit()
async def pin_active_event(event_id: int):
    for event in await get_all_events():
        await deactivate_event(event.id)
    await activate_event(event_id)
async def get_all_events():
    async with async_session() as session:
        result = await session.execute(select(Event))
        return result.scalars().all()

async def get_event_by_id(event_id: int):
    async with async_session() as session:
        result = await session.execute(select(Event).where(Event.id == event_id))
        return result.scalar_one_or_none()
async def delete_event(event_id: int):
    async with async_session() as session:
        await session.execute(delete(Event).where(Event.id == event_id))
        await session.commit()
async def get_latest_event_link_for_user(telegram_user_id: int) -> str | None:
    """
    Foydalanuvchining eng oxirgi qo'shilgan eventining linkini qaytaradi.
    Agar qo'shilgan event bo'lmasa, None qaytaradi.
    """
    async with async_session() as session:
        # Eng oxirgi qo'shilgan eventni topamiz (joined_at bo'yicha tartiblab)
        result = await session.execute(
            select(Event.link)
            .join(EventParticipant, EventParticipant.event_id == Event.id)
            .where(EventParticipant.telegram_user_id == telegram_user_id)
            .order_by(desc(EventParticipant.joined_at))
            .limit(1)
        )
        
        latest_event = result.scalar_one_or_none()
        return latest_event