from aiogram import Dispatcher

from .card_pay import register_card_pay
from .private_link import register_private_link
from .user import register_user


def register_all_user_handlers(dp: Dispatcher):
    register_user(dp)
    register_private_link(dp)
    register_card_pay(dp)