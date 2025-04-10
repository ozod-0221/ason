from aiogram import Router, F,Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import *
from database.db_utils import *
from config import *
from inline_keyboard import *
import asyncio
import logging
import os
from aiogram.types import FSInputFile

from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link
admin_filter = F.from_user.id.in_(ADMIN_IDS)
admin_router = Router()


  # o‘zingni telegram ID bilan almashtir
@admin_router.message(admin_filter, F.text == "🎁Event yaratish")
@admin_router.message(admin_filter,F.text == "/add_event")
async def start_add_event(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        return await message.answer("Bu buyruq faqat adminlar uchun.")
    
    await state.set_state(AddEventState.waiting_for_name)
    await message.answer("Yangi event nomini kiriting:")

@admin_router.message(AddEventState.waiting_for_name)
async def get_event_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddEventState.waiting_for_link)
    await message.answer("Endi translyatsiya uchun linkini kiriting:")
@admin_router.message(AddEventState.waiting_for_link)
async def get_referral_id(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await state.set_state(AddEventState.waiting_for_referral_id)
    await message.answer("Endi referal ID ni kiriting (masalan: `promo2025`)")
    
@admin_router.message(AddEventState.waiting_for_referral_id)
async def get_referral_id(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    referral_id = message.text
    link = data["link"]
    success = await add_event(name, referral_id,link)
    if success:
        referral_link=f"https://t.me/{BOT_USERNAME}?start={referral_id}"
        await message.answer(f"✅ Event qo‘shildi:\n📌 Nomi: {name}\n🔗 Referral ID: {referral_id}")
        await message.answer(f"refferal link:\n{referral_link} ")
    else:
        await message.answer("❌ Bu referral ID allaqachon mavjud. Qaytadan urinib ko‘ring.")
    
    await state.clear()
@admin_router.message(admin_filter,F.text == "📊 Statistikalar")
async def get_stats(message: Message):
    
    
    # Statistikalarni olish
    try:
        events = await get_statistics()
    except Exception as e:
        logging.error(f"Error fetching statistics: {e}")
        await message.answer("Statistikalarni olishda xatolik yuz berdi.")
        return

    # Boshlang'ich matnni yaratish
    text = " "
    
    # Har bir eventni formatlash
    for event in events:
        try:
            count_of_participants = await get_participant_count_by_referral(event.events_referal_id)
        except Exception as e:
            logging.error(f"Error fetching participant count: {e}")
        referal_link = f"https://t.me/{BOT_USERNAME}?start={event.events_referal_id}"
        text = f"\n📕Event_nomi: {event.name}\n🔗Referal kodi: {event.events_referal_id}\n➕Qatnashuvchilar soni: {count_of_participants}\nTranslyatsiya linki:{event.link}\n👀👀👀👀👀👀👀👀👀👀👀👀\n{referal_link}"
    
    # Natijani yuborish
        await message.answer(text,reply_markup=await settings_statistics_inline_keyboard(event.id))
@admin_router.message(admin_filter,F.text == "💬 Xabar yuborish")
async def send_message(message: Message,state: FSMContext):
    await message.answer("Kanaldagi postning URL manzilini kiriting:")
    await state.set_state(SendMessageState.waiting_for_post_link)
@admin_router.message(SendMessageState.waiting_for_post_link)
async def forward_message(message: Message, state: FSMContext,bot:Bot):
    post_link = message.text
    message_id = post_link.split("/")[-1]
    # Kanaldagi postni olish
    for user_id in await get_all_user_ids():
        try:
            await bot.forward_message(user_id,CHANNEL_ID,  message_id)
            await asyncio.sleep(0.3)
        except Exception as e:
            logging.error(f"Xatolik sodir bo'ldi: {e}")
    await message.answer("Xabar yuborildi!")
    
    await state.clear()
    
@admin_router.callback_query(F.data.startswith("statistics_users_"))
async def handle_export_participants(callback: CallbackQuery, bot: Bot):
    try:
        event_id = int(callback.data.split("_")[2])
        await callback.answer("Excel fayl tayyorlanmoqda...", show_alert=False)
        
        filename = await export_participants_to_excel(event_id)
        
        if not filename:
            await callback.message.answer("Bu eventda hali qatnashchilar yo'q")
            return

        # Faylni to'g'ri formatda yuborish
        document = FSInputFile(filename)
        
        await callback.message.answer_document(
            document=document,
            caption=f"Event {event_id} qatnashchilari ro'yxati"
        )
        
        # Faylni o'chirish
        os.remove(filename)
            
    except Exception as e:
        await callback.message.answer(f"Xatolik yuz berdi: {str(e)}")
        await callback.answer("Xatolik yuz berdi!", show_alert=True)

@admin_router.callback_query(F.data.startswith("pin_"))
async def handle_pin_event(callback: CallbackQuery, bot: Bot):
    event_id = int(callback.data.split("_")[1])
    await callback.answer("bajarildi", show_alert=True)
    try:
        await pin_active_event(event_id)
        
        await callback.message.answer("Event faollashtirildi")
    except Exception as e:
        await callback.message.answer(f"Xatolik yuz berdi: {str(e)}")
        await callback.answer("Xatolik yuz berdi!", show_alert=True)
@admin_router.message(admin_filter,F.text.startswith("activate_event_"))
async def activate_events(message: Message):
    event_id = int(message.text.split("_")[2])
    try:
        await activate_event(event_id)
        await message.answer("Event faollashtirildi")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")
@admin_router.callback_query(F.data.startswith("delete_event_"))
async def delete_events(callback: CallbackQuery):
    event_id = int(callback.data.split("_")[2])
   
    try:
        await delete_event(event_id)
        await callback.answer("Event o'chirildi", show_alert=True)
        await callback.message.answer("Event o'chirildi")
        
    except Exception as e:
        await callback.message.answer(f"Xatolik yuz berdi: {str(e)}")
        print(f"Xatolik yuz berdi: {str(e)}")
        await callback.answer("Xatolik yuz berdi!", show_alert=True)