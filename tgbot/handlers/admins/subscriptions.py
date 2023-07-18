import time

from aiogram import Dispatcher
from aiogram.types import ContentType, CallbackQuery, PreCheckoutQuery, Message

from tgbot.config import PAYMENT_TOKEN, days_to_seconds, db
from tgbot.filters.is_ban import IsBanFilter
from tgbot.misc.keyboards import submonthmenu_inline, subhalfyear_inline, cancel_inline
from tgbot.misc.states import PromoCodeState


async def sub_month_menu(call: CallbackQuery):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_message(call.from_user.id, '<b>Месяц\nЦена: 300р\nСрок подписки: 1 месяц</b>\n\n'
                                                   'Вы получите приглашение в канал/чат 👇\n<b>- ТРАНСФЕР-МОСТ Заказы</b>',
                                reply_markup=submonthmenu_inline)


async def sub_half_year_menu(call: CallbackQuery):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_message(call.from_user.id, '<b>Месяц\nЦена: 600р\nСрок подписки: 6 месяцев</b>\n\n'
                                                   'Вы получите приглашение в канал/чат 👇\n<b>- ТРАНСФЕР-МОСТ Заказы</b>',
                                reply_markup=subhalfyear_inline)


async def promocode(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, 'Отправьте боту ваш промокод для скидки: ', reply_markup=cancel_inline)
    await PromoCodeState.code.set()


async def promocode_state(message: Message): # TODO НАДО ДОДЕЛАТЬ ЭТУ ЧАСТЬ
    if not db.is_promo_code_used(message.from_user.id, message.text):
        discount = db.get_discount(message.text)
        if discount is not None:
            pass



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
        await message.bot.send_message(message.from_user.id, "Вам выдана подписка на месяц!\n"
                                                             "Вы получили приглашение в канал/чат 👇\n"
                                                             "<b>- ТРАНСФЕР-МОСТ Заказы</b>\n"
                                                             "https://t.me/+VHuzPV-cvZlkZWQy\n\n"
                                                             "Для перехода в главное меню, отправьте боту команду - /start.")
    elif message.successful_payment.invoice_payload == "halfyear_sub":
        time_sub = int(time.time()) + days_to_seconds(180)
        db.set_time_sub(message.from_user.id, time_sub)
        await message.bot.send_message(message.from_user.id, "Вам выдана подписка на полгода!"
                                                             "Вы получили приглашение в канал/чат 👇\n"
                                                             "<b>- ТРАНСФЕР-МОСТ Заказы</b>\n"
                                                             "https://t.me/+VHuzPV-cvZlkZWQy\n\n"
                                                             "Для перехода в главное меню, отправьте боту команду - /start.")


def register_subscription_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        sub_month_menu, IsBanFilter(), text='submonthmenu', state='*'
    )
    dp.register_callback_query_handler(
        sub_half_year_menu, IsBanFilter(), text='subhalfyearmenu', state='*'
    )
    dp.register_callback_query_handler(
        promocode, IsBanFilter(), text='promocode', state='*'
    )
    dp.register_message_handler(
        promocode_state, IsBanFilter(), state=PromoCodeState.code
    )
    dp.register_callback_query_handler(
        sub_month, IsBanFilter(), text="submonth", state='*'
    )
    dp.register_callback_query_handler(
        sub_half_year, IsBanFilter(), text="subhalfyear", state='*'
    )
    dp.register_pre_checkout_query_handler(
        process_pre_checkout_query, IsBanFilter(), state='*'
    )
    dp.register_message_handler(
        process_pay, IsBanFilter(), content_types=ContentType.SUCCESSFUL_PAYMENT, state='*'
    )
