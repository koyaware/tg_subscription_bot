import time

from aiogram import Dispatcher
from aiogram.types import ContentType, CallbackQuery, PreCheckoutQuery, Message

from tgbot.config import PAYMENT_TOKEN, days_to_seconds, db


async def sub_month(call: CallbackQuery):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_invoice(chat_id=call.from_user.id, title="Оформление подписки",
                           description="Тестовое описание товара", payload="month_sub",
                           provider_token=PAYMENT_TOKEN, currency="RUB",
                           start_parameter="test_bot", prices=[{"label": "Руб", "amount": 30000}])


async def sub_half_year(call: CallbackQuery):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_invoice(chat_id=call.from_user.id, title="Оформление подписки",
                           description="Тестовое описание товара", payload="halfyear_sub",
                           provider_token=PAYMENT_TOKEN, currency="RUB",
                           start_parameter="test_bot", prices=[{"label": "Руб", "amount": 60000}])


async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_pay(message: Message):
    if message.successful_payment.invoice_payload == "month_sub":
        time_sub = int(time.time()) + days_to_seconds(30)
        db.set_time_sub(message.from_user.id, time_sub)
        await message.bot.send_message(message.from_user.id, "Вам выдана подписка на месяц!")
    elif message.successful_payment.invoice_payload == "halfyear_sub":
        time_sub = int(time.time()) + days_to_seconds(180)
        db.set_time_sub(message.from_user.id, time_sub)
        await message.bot.send_message(message.from_user.id, "Вам выдана подписка на полгода!")


def register_subscription_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        sub_month, text="submonth"
    )
    dp.register_callback_query_handler(
        sub_half_year, text="subhalfyear"
    )
    dp.register_pre_checkout_query_handler(
        process_pre_checkout_query
    )
    dp.register_message_handler(
        process_pay, content_types=ContentType.SUCCESSFUL_PAYMENT
    )
