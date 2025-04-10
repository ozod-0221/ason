# handlers/start.py
from aiogram import Router, F
from aiogram.types import Message
from config import ADMIN_IDS
from handlers.admin import admin_router
from handlers.user import user_router
from database.db_utils import *
from database.db import async_session
from database.models import Event, EventParticipant, User
from sqlalchemy import select
from datetime import datetime
from inline_keyboard import *
from reply_keyboard import *
from datetime import datetime
from states import *
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link

start_router = Router()

@start_router.message(F.text.startswith("/start"))
async def handle_start(message: Message,state:FSMContext):
    user_id = message.from_user.id
    full_name = message.from_user.full_name 
    
    # Referal kodni ajratib olish
    data = message.text.split()
    referal_code = data[1] if len(data) > 1 else None
    
    if not await user_exists(user_id):
        # Yangi foydalanuvchini bazaga qo'shish
        try:
            await add_user(
                telegram_user_id=user_id,
                name=full_name,
                role=RoleEnum.USER,
                phone_number=None
            )
        except Exception as e:
            print(f"userni bazaga qo'shishda xatolik: {e}")

    if referal_code:
        print(f"Referal kod: {referal_code}")
        try:
            event_exists = await exist_event(referal_code)
            if event_exists:
                """user_in_event = await user_exist_in_event(user_id, referal_code)
                if not user_in_event:"""
                try:
                        # Avval eventni ID sini olishimiz kerak
                    event = await get_event_by_referral_id(referal_code)
                    if event:
                        await add_event_participant(
                                telegram_user_id=user_id,
                                event_id=event.id,  # event.id ni yuboramiz
                                joined_at=datetime.now()
                            )
                        
                        print("Foydalanuvchi eventga qo'shildi")
                except Exception as e:
                        print(f"userni eventga qo'shishda xatolik: {e}")
                """else:
                    print("Foydalanuvchi allaqachon ushbu eventga qo'shilgan")"""
            else:
                print("Bunday referal kod topilmadi")
        except Exception as e:
            print(f"Eventni tekshirishda xatolik: {e}")
        print("📍📍📍📍📍📍📍📍📍📍")
        print(referal_code)
    else:
        print("Oddiy start")
        active_event=await get_active_event()
        link=active_event.link
        

    if user_id in ADMIN_IDS:
        await message.answer("👑 Siz adminsiz! Menyuni tanlang.", reply_markup=admin_keyboard())
    else:
        name = message.from_user.first_name or "Foydalanuvchi"
        await state.set_state(OrderStates.waiting_for_contact)
        await message.answer(f"Assalomu alekum {name}, Xush kelibsiz!", reply_markup=contact_keyboard())
        await state.update_data(active_link=link)
