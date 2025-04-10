from aiogram.types import InlineKeyboardMarkup,InaccessibleMessage,InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import *
from database.db_utils import *

def  subs_key() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="↗️Instagram",url=INSTAGRAM_URL),
        InlineKeyboardButton(text="↗️Telegram",url=TG_CHANNEL_URL),

        InlineKeyboardButton(text="✅Tekshirish",callback_data="check"),
    )
    builder.adjust(1)
    return builder.as_markup()
def forward_message_key(id)-> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Ulashish",switch_inline_query=id),
    )
    builder.adjust(1)
    return builder.as_markup()
async def settings_statistics_inline_keyboard(event_id):
    builder = InlineKeyboardBuilder()
    event=await get_event_by_id(event_id)
    if event.is_active:
    
        builder.add(
            InlineKeyboardButton(text="👤 Foydalanuvchilar",callback_data=f"statistics_users_{event_id}"),
            InlineKeyboardButton(text="🗑 O'chirish",callback_data=f"delete_event_{event_id}"),
            InlineKeyboardButton(text="📍 Mahkamlangan",callback_data=f"pin_{event_id}")
        )
    else:
        builder.add(
            InlineKeyboardButton(text="👤 Foydalanuvchilar",callback_data=f"statistics_users_{event_id}"),
            InlineKeyboardButton(text="🗑 O'chirish",callback_data=f"delete_event_{event_id}"),
            InlineKeyboardButton(text="Faollashtirish",callback_data=f"pin_{event_id}")
        )
    builder.adjust(1)
    return builder.as_markup()  
