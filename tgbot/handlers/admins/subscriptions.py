import time

from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.config import days_to_seconds, db, ADMIN_IDS
from tgbot.filters.is_ban import IsBanFilter
from tgbot.misc.keyboards import submonthmenu_inline, subhalfyear_inline, subweekmenu_inline, subfreemenu_inline, \
    subthreemonthmenu_inline, sub_link_inline


async def sub_free_menu(call: CallbackQuery):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_message(call.from_user.id, '<b>14 дней (2 недели)\nЦена: 0р\nСрок подписки: 2 недели</b>\n\n'
                                                   'Вы получите приглашение в канал/чат 👇\n<b>- ТРАНСФЕР-МОСТ Заказы</b>',
                                reply_markup=subfreemenu_inline)


async def sub_free(call: CallbackQuery):
    status = db.get_active_status(call.from_user.id)
    if status is False:
        db.set_active_status(call.from_user.id, 1)
        time_sub = int(time.time()) + days_to_seconds(14)
        db.set_time_sub(call.from_user.id, time_sub)
        await call.bot.edit_message_text("Вам выдана подписка на месяц!\n"
                                         "Вы получили приглашение в канал/чат 👇\n"
                                         "<b>- ТРАНСФЕР-МОСТ Заказы</b>\n"
                                         "Для перехода в главное меню, отправьте боту команду"
                                         " - /start.",
                                         call.message.chat.id, call.message.message_id,
                                         reply_markup=sub_link_inline,)
        for admin in ADMIN_IDS:
            await call.bot.send_message(admin, f"💰 Новая подписка.\n"
                                               f"\nПользователь: @{call.from_user.username}, <b>{call.from_user.first_name}</b>\n"
                                               f"[ID:{call.from_user.id}] только что оформил подписку на 14 дней (2 недели)."
                                               f"\n\nСрок подписки: <b>14 дней.</b>")
    else:
        return await call.bot.edit_message_text('Вы уже использовали пробную подписку!',
                                                call.message.chat.id, call.message.message_id)


async def sub_week_menu(call: CallbackQuery):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_message(call.from_user.id, '<b>Неделя\nЦена: 150р\nСрок подписки: 1 неделя</b>\n\n'
                                                   'Вы получите приглашение в канал/чат 👇\n<b>- ТРАНСФЕР-МОСТ Заказы</b>',
                                reply_markup=subweekmenu_inline)


async def sub_month_menu(call: CallbackQuery):
    await call.bot.edit_message_text('<b>Месяц\nЦена: 150р\nСрок подписки: 1 месяц</b>\n\n'
                                     'Вы получите приглашение в канал/чат 👇\n<b>- ТРАНСФЕР-МОСТ Заказы</b>',
                                     call.message.chat.id, call.message.message_id,
                                     reply_markup=submonthmenu_inline)


async def sub_three_month_menu(call: CallbackQuery):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_message(call.from_user.id, '<b>3 месяца\nЦена: 300р\nСрок подписки: 3 месяца</b>\n\n'
                                                   'Вы получите приглашение в канал/чат 👇\n<b>- ТРАНСФЕР-МОСТ Заказы</b>',
                                reply_markup=subthreemonthmenu_inline)


async def sub_half_year_menu(call: CallbackQuery):
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_message(call.from_user.id, '<b>6 месяцев / Полгода\nЦена: 550р\nСрок подписки: 6 месяцев</b>\n\n'
                                                   'Вы получите приглашение в канал/чат 👇\n<b>- ТРАНСФЕР-МОСТ Заказы</b>',
                                reply_markup=subhalfyear_inline)


# ЭТО ПЛАТЕЖКА ЧЕРЕЗ ЮМАНЕЙ, НО ВИДИМО БОЛЬШЕ НЕ НУЖНАЯ.
# async def sub_week(call: CallbackQuery):
#     await call.bot.delete_message(call.from_user.id, call.message.message_id)
#     await call.bot.send_invoice(chat_id=call.from_user.id, title="Оформление подписки",
#                            description="Вы получите приглашение в канал/чат 👇\n- ТРАНСФЕР-МОСТ Заказы", payload="week_sub",
#                            provider_token=PAYMENT_TOKEN, currency="RUB",
#                            start_parameter="sub_week", prices=[{"label": "Руб", "amount": 15000}])
#
#
# async def sub_month(call: CallbackQuery):
#     await call.bot.delete_message(call.from_user.id, call.message.message_id)
#     await call.bot.send_invoice(chat_id=call.from_user.id, title="Оформление подписки",
#                            description="Вы получите приглашение в канал/чат 👇\n- ТРАНСФЕР-МОСТ Заказы", payload="month_sub",
#                            provider_token=PAYMENT_TOKEN, currency="RUB",
#                            start_parameter="sub_month", prices=[{"label": "Руб", "amount": 15000}])
#
#
# async def sub_three_month(call: CallbackQuery):
#     await call.bot.delete_message(call.from_user.id, call.message.message_id)
#     await call.bot.send_invoice(chat_id=call.from_user.id, title="Оформление подписки",
#                            description="Вы получите приглашение в канал/чат 👇\n- ТРАНСФЕР-МОСТ Заказы", payload="three_month_sub",
#                            provider_token=PAYMENT_TOKEN, currency="RUB",
#                            start_parameter="three_month_sub", prices=[{"label": "Руб", "amount": 30000}])
#
#
# async def sub_half_year(call: CallbackQuery):
#     await call.bot.delete_message(call.from_user.id, call.message.message_id)
#     await call.bot.send_invoice(chat_id=call.from_user.id, title="Оформление подписки",
#                            description="Вы получите приглашение в канал/чат 👇\n- ТРАНСФЕР-МОСТ Заказы", payload="halfyear_sub",
#                            provider_token=PAYMENT_TOKEN, currency="RUB",
#                            start_parameter="sub_half_year", prices=[{"label": "Руб", "amount": 50000}])
#
#
# async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
#     await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
#
#
# async def process_pay(message: Message):
#     if message.successful_payment.invoice_payload == "month_sub":
#         time_sub = int(time.time()) + days_to_seconds(30)
#         db.set_time_sub(message.from_user.id, time_sub)
#         await message.bot.send_message(message.from_user.id, "Вам выдана подписка на месяц!\n"
#                                                              "Вы получили приглашение в канал/чат 👇\n"
#                                                              "<b>- ТРАНСФЕР-МОСТ Заказы</b>\n"
#                                                              "Для перехода в главное меню, отправьте боту команду"
#                                                              " - /start.", reply_markup=sub_link_inline)
#         for admin in ADMIN_IDS:
#             await message.bot.send_message(admin, f"💰 Новая подписка.\n"
#                                                   f"\nПользователь: @{message.from_user.username}, <b>{message.from_user.first_name}</b>\n"
#                                                   f"[ID:{message.from_user.id}] только что оформил подписку на месяц."
#                                                   f"\n\nСрок подписки: 30 дней.")
#     elif message.successful_payment.invoice_payload == 'three_month_sub':
#         time_sub = int(time.time()) + days_to_seconds(90)
#         db.set_time_sub(message.from_user.id, time_sub)
#         await message.bot.send_message(message.from_user.id, "Вам выдана подписка на 3 месяца!\n"
#                                                              "Вы получили приглашение в канал/чат 👇\n"
#                                                              "<b>- ТРАНСФЕР-МОСТ Заказы</b>\n"
#                                                              "Для перехода в главное меню, отправьте боту команду"
#                                                              " - /start.", reply_markup=sub_link_inline)
#         for admin in ADMIN_IDS:
#             await message.bot.send_message(admin, f"💰 Новая подписка.\n"
#                                                   f"\nПользователь: @{message.from_user.username}, <b>{message.from_user.first_name}</b>\n"
#                                                   f"[ID:{message.from_user.id}] только что оформил подписку на 3 месяца."
#                                                   f"\n\nСрок подписки: 90 дней.")
#     elif message.successful_payment.invoice_payload == "halfyear_sub":
#         time_sub = int(time.time()) + days_to_seconds(180)
#         db.set_time_sub(message.from_user.id, time_sub)
#         await message.bot.send_message(message.from_user.id, "Вам выдана подписка на полгода!"
#                                                              "Вы получили приглашение в канал/чат 👇\n"
#                                                              "<b>- ТРАНСФЕР-МОСТ Заказы</b>\n"
#                                                              "Для перехода в главное меню, отправьте боту команду"
#                                                              " - /start.", reply_markup=sub_link_inline)
#         for admin in ADMIN_IDS:
#             await message.bot.send_message(admin, f"💰 Новая подписка.\n"
#                                                   f"\nПользователь: @{message.from_user.username}, <b>{message.from_user.first_name}</b>\n"
#                                                   f"[ID:{message.from_user.id}] только что оформил подписку на полгода."
#                                                   f"\n\nСрок подписки: 180 дней.")
#     elif message.successful_payment.invoice_payload == "week_sub":
#         time_sub = int(time.time()) + days_to_seconds(7)
#         db.set_time_sub(message.from_user.id, time_sub)
#         await message.bot.send_message(message.from_user.id, "Вам выдана подписка на неделю!"
#                                                              "Вы получили приглашение в канал/чат 👇\n"
#                                                              "<b>- ТРАНСФЕР-МОСТ Заказы</b>\n"
#                                                              "Для перехода в главное меню, отправьте боту команду"
#                                                              " - /start.", reply_markup=sub_link_inline)
#         for admin in ADMIN_IDS:
#             await message.bot.send_message(admin, f"💰 Новая подписка.\n"
#                                                   f"\nПользователь: @{message.from_user.username}, <b>{message.from_user.first_name}</b>\n"
#                                                   f"[ID:{message.from_user.id}] только что оформил подписку на неделю."
#                                                   f"\n\nСрок подписки: 7 дней.")


def register_subscription_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        sub_free_menu, IsBanFilter(), text='subfreemenu', state='*'
    )
    dp.register_callback_query_handler(
        sub_free, IsBanFilter(), text='subfree', state='*'
    )
    dp.register_callback_query_handler(
        sub_week_menu, IsBanFilter(), text='subweekmenu', state='*'
    )
    dp.register_callback_query_handler(
        sub_month_menu, IsBanFilter(), text='submonthmenu', state='*'
    )
    dp.register_callback_query_handler(
        sub_three_month_menu, IsBanFilter(), text='subthreemonthmenu', state='*'
    )
    dp.register_callback_query_handler(
        sub_half_year_menu, IsBanFilter(), text='subhalfyearmenu', state='*'
    )
    # dp.register_callback_query_handler(
    #     sub_week, IsBanFilter(), text='subweek', state='*'
    # )
    # dp.register_callback_query_handler(
    #     sub_month, IsBanFilter(), text="submonth", state='*'
    # )
    # dp.register_callback_query_handler(
    #     sub_half_year, IsBanFilter(), text="subhalfyear", state='*'
    # )
    # dp.register_pre_checkout_query_handler(
    #     process_pre_checkout_query, IsBanFilter(), state='*'
    # )
    # dp.register_message_handler(
    #     process_pay, IsBanFilter(), content_types=ContentType.SUCCESSFUL_PAYMENT, state='*'
    # )
