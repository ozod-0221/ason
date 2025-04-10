from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📦Qo`llanmani olish"),
            ],
            [
                KeyboardButton(text="👤 Profil"),
                KeyboardButton(text="💬 Biz haqimizda"),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard
def back_to_main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🏠 Bosh menu"),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard
def cancel_order_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="❌ Bekor qilish"),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard
def contact_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="☎️Kontaktni ulashish", request_contact=True))
    builder.add(KeyboardButton(text="✖️Bekor qilish"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
def admin_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🎁Event yaratish"))
    builder.add(KeyboardButton(text="💬 Xabar yuborish"))
    builder.add(KeyboardButton(text="📊 Statistikalar"))
    
    
    
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
