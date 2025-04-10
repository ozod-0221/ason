from aiogram.types import Contact, Message
import logging
from aiogram import Bot
from config import CHANNEL_ID
def has_digit(s: str) -> bool:
    return any(char.isdigit() for char in s)

def is_true_contact(contact: Contact,message: Message) -> bool:
    if contact.first_name== message.from_user.first_name :
        return True
    elif contact.last_name== message.from_user.last_name:
        return True
    elif contact.first_name== message.from_user.last_name:
        return True
    elif contact.last_name== message.from_user.first_name:
        return True
    else:
        return False
async def save_anyWord(link:str,user_id: int,DateTime:str):
    class Word:
        def __init__(self, word, user_id, DateTime):
            self.word = word
            self.user_id = user_id
            self.DateTime = DateTime
        def __str__(self):
            return f"Word: {self.word}, User ID: {self.user_id}, DateTime: {self.DateTime}"
        
    
