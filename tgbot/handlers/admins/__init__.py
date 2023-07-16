from aiogram import Dispatcher

from .admin import register_admin
from .feedback import register_feedback_handlers
from .rates import register_rates
from .subscriptions import register_subscription_handlers


def register_admin_handlers(dp: Dispatcher):
    register_admin(dp)
    register_feedback_handlers(dp)
    register_subscription_handlers(dp)
    register_rates(dp)