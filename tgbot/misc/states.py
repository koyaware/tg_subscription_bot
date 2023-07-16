from aiogram.dispatcher.filters.state import StatesGroup, State


class FeedbackState(StatesGroup):
    waiting_for_message = State()
    waiting_for_admin_message = State()


class RatesState(StatesGroup):
    message = State()
    ban_id = State()
