from aiogram.fsm.state import State, StatesGroup

class AddEventState(StatesGroup):
    waiting_for_name = State()
    waiting_for_referral_id = State()
    waiting_for_link = State()
class OrderStates(StatesGroup):
    
    waiting_for_contact = State()
    waiting_for_subscription = State()
class SendMessageState(StatesGroup):
    waiting_for_post_link = State()
    