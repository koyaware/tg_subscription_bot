import json
import time

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.config import ADMIN_IDS, connect_to_redis, days_to_seconds, db
from tgbot.filters import AdminFilter
from tgbot.filters.is_ban import IsBanFilter
from tgbot.misc.keyboards import sub_pay_card_sure_inline, sub_success_or_ban_inline, \
    sub_link_inline, sub_pay_month_card_inline, sub_pay_three_month_card_inline, sub_pay_half_year_card_inline
from tgbot.misc.states import SubPayCardState


async def sub_pay_month_card(call: CallbackQuery):
    await call.message.bot.edit_message_text('Тариф: <b>Месяц</b>\nСпособ оплаты:'
                                             ' <b>Перевод по номеру телефона</b>\nСумма к отплате: <b>150₽.</b>'
                                             '\nИнформация об оплате:\nТинков <code>89124436363</code>'
                                             '\nСкрин чека отправить админу, либо сюда же в бота',
                                             call.message.chat.id, call.message.message_id,
                                             reply_markup=sub_pay_month_card_inline)


async def sub_pay_three_month_card(call: CallbackQuery):
    await call.message.bot.edit_message_text('Тариф: <b>3 месяца</b>\nСпособ оплаты:'
                                             ' <b>Перевод по номеру телефона</b>\nСумма к отплате: <b>300₽.</b>'
                                             '\nИнформация об оплате:\nТинков <code>89124436363</code>'
                                             '\nСкрин чека отправить админу, либо сюда же в бота',
                                             call.message.chat.id, call.message.message_id,
                                             reply_markup=sub_pay_three_month_card_inline)


async def sub_pay_half_year_card(call: CallbackQuery):
    await call.message.bot.edit_message_text('Тариф: <b>Полгода</b>\nСпособ оплаты:'
                                             ' <b>Перевод по номеру телефона</b>\nСумма к отплате: <b>550₽.</b>'
                                             '\nИнформация об оплате:\nТинков <code>89124436363</code>'
                                             '\nСкрин чека отправить админу, либо сюда же в бота',
                                             call.message.chat.id, call.message.message_id,
                                             reply_markup=sub_pay_half_year_card_inline)


async def sub_pay_month_card_sure(call: CallbackQuery):
    for admin in ADMIN_IDS:
        await call.bot.send_message(admin, f"\nПользователь: @{call.from_user.username}, "
                                           f"<b>{call.from_user.first_name}</b>\n"
                                           f"[ID:{call.from_user.id}] вызвал оплату тарифа: "
                                           f"<b>Месяц</b>\nСумма к оплате: "
                                           f"<b>150₽.</b>\nСпособ оплаты: <b>Полуавтоматический "
                                           f"[Перевод по номеру телефона]</b>")
    await call.bot.edit_message_text('💰 <b>Оплатили?</b>\n\nОтправьте боту квинтацию об '
                                     'оплате: <b>скриншот или фото.</b>\n'
                                     'На квинтации должны быть четко видны: <b>'
                                     'дата, время и сумма платежа.</b>\n'
                                     '<code>Или вы можете отправить точную дату и время платежа</code>',
                                        call.message.chat.id, call.message.message_id,
                                        reply_markup=sub_pay_card_sure_inline)
    await SubPayCardState.pay_month.set()


async def sub_pay_month_card_state(message: Message, state: FSMContext):
    for admin in ADMIN_IDS:
        if isinstance(message.text, str):
            await message.bot.copy_message(chat_id=admin, from_chat_id=message.from_user.id,
                                           message_id=message.message_id)
            await message.bot.send_message(admin, f"💰 Подтвердите покупку.\n"
                                                  f"\nПользователь: @{message.from_user.username}, "
                                                  f"<b>{message.from_user.first_name}</b>\n"
                                                  f"[ID:{message.from_user.id}]\nТариф: <b>Месяц</b>\nСумма к оплате: "
                                                  f"<b>150₽.</b>\nПлатежная система: <b>Перевод по номеру телефона</b>",
                                           reply_markup=sub_success_or_ban_inline)
        else:
            await message.bot.copy_message(chat_id=admin, from_chat_id=message.from_user.id,
                                           message_id=message.message_id,
                                           caption=f"💰 Подтвердите покупку.\n"
                                                   f"\nПользователь: @{message.from_user.username},"
                                                   f" <b>{message.from_user.first_name}</b>\n"
                                                   f"[ID:{message.from_user.id}]\nТариф: <b>Месяц</b>\nСумма к оплате: "
                                                   f"<b>150₽.</b>\nПлатежная система: <b>Перевод по номеру телефона</b>"
                                           , reply_markup=sub_success_or_ban_inline)
    await message.bot.send_message(message.from_user.id, '✅ Спасибо! Квитанция отправлена на проверку, вы получите '
                                                         'уведомление как только её проверят.')
    await state.finish()
    redis_pool = await connect_to_redis()
    user_data = {
        'first_name': message.from_user.first_name,
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'season': 'месяц',
        'exact_time': '30'
    }
    user_data_str = json.dumps(user_data)
    await redis_pool.set(name='user_data', value=user_data_str)


async def sub_pay_three_month_card_sure(call: CallbackQuery):
    for admin in ADMIN_IDS:
        await call.bot.send_message(admin, f"\nПользователь: @{call.from_user.username}, "
                                           f"<b>{call.from_user.first_name}</b>\n"
                                           f"[ID:{call.from_user.id}] вызвал оплату тарифа: "
                                           f"<b>3 месяца.</b>\nСумма к оплате: "
                                           f"<b>300₽.</b>\nСпособ оплаты: <b>Полуавтоматический "
                                           f"[Перевод по номеру телефона]</b>")
    await call.bot.edit_message_text('💰 <b>Оплатили?</b>\n\nОтправьте боту квинтацию об '
                                     'оплате: <b>скриншот или фото.</b>\n'
                                     'На квинтации должны быть четко видны: <b>'
                                     'дата, время и сумма платежа.</b>\n'
                                     '<code>Или вы можете отправить точную дату и время платежа</code>',
                                        call.message.chat.id, call.message.message_id,
                                        reply_markup=sub_pay_card_sure_inline)
    await SubPayCardState.pay_three_month.set()


async def sub_pay_three_month_card_state(message: Message, state: FSMContext):
    for admin in ADMIN_IDS:
        if isinstance(message.text, str):
            await message.bot.copy_message(chat_id=admin, from_chat_id=message.from_user.id,
                                           message_id=message.message_id)
            await message.bot.send_message(admin, f"💰 Подтвердите покупку.\n"
                                                  f"\nПользователь: @{message.from_user.username}, "
                                                  f"<b>{message.from_user.first_name}</b>\n"
                                                  f"[ID:{message.from_user.id}]\nТариф: <b>3 месяца.</b>"
                                                  f"\nСумма к оплате: "
                                                  f"<b>300₽.</b>\nПлатежная система: <b>Перевод по номеру телефона</b>",
                                           reply_markup=sub_success_or_ban_inline)
        else:
            await message.bot.copy_message(chat_id=admin, from_chat_id=message.from_user.id,
                                           message_id=message.message_id,
                                           caption=f"💰 Подтвердите покупку.\n"
                                                   f"\nПользователь: @{message.from_user.username},"
                                                   f" <b>{message.from_user.first_name}</b>\n"
                                                   f"[ID:{message.from_user.id}]\nТариф: <b>3 месяца.</b>"
                                                   f"\nСумма к оплате: "
                                                   f"<b>300₽.</b>\nПлатежная система: <b>Перевод по номеру телефона</b>"
                                           , reply_markup=sub_success_or_ban_inline)
    await message.bot.send_message(message.from_user.id, '✅ Спасибо! Квитанция отправлена на проверку, вы получите '
                                                         'уведомление как только её проверят.')
    await state.finish()
    redis_pool = await connect_to_redis()
    user_data = {
        'first_name': message.from_user.first_name,
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'season': '3 месяца',
        'exact_time': '90'
    }
    user_data_str = json.dumps(user_data)
    await redis_pool.set(name='user_data', value=user_data_str)


async def sub_pay_half_year_card_sure(call: CallbackQuery):
    for admin in ADMIN_IDS:
        await call.bot.send_message(admin, f"\nПользователь: @{call.from_user.username}, "
                                           f"<b>{call.from_user.first_name}</b>\n"
                                           f"[ID:{call.from_user.id}] вызвал оплату тарифа: "
                                           f"<b>Полгода</b>\nСумма к оплате: "
                                           f"<b>550₽.</b>\nСпособ оплаты: <b>Полуавтоматический "
                                           f"[Перевод по номеру телефона]</b>")
    await call.bot.edit_message_text('💰 <b>Оплатили?</b>\n\nОтправьте боту квинтацию об '
                                     'оплате: <b>скриншот или фото.</b>\n'
                                     'На квинтации должны быть четко видны: <b>'
                                     'дата, время и сумма платежа.</b>\n'
                                     '<code>Или вы можете отправить точную дату и время платежа</code>',
                                        call.message.chat.id, call.message.message_id,
                                        reply_markup=sub_pay_card_sure_inline)
    await SubPayCardState.pay_half_year.set()


async def sub_pay_half_year_card_state(message: Message, state: FSMContext):
    for admin in ADMIN_IDS:
        if isinstance(message.text, str):
            await message.bot.copy_message(chat_id=admin, from_chat_id=message.from_user.id,
                                           message_id=message.message_id)
            await message.bot.send_message(admin, f"💰 Подтвердите покупку.\n"
                                                  f"\nПользователь: @{message.from_user.username}, "
                                                  f"<b>{message.from_user.first_name}</b>\n"
                                                  f"[ID:{message.from_user.id}]\nТариф: <b>Полгода</b>\nСумма к оплате: "
                                                  f"<b>550₽.</b>\nПлатежная система: <b>Перевод по номеру телефона</b>",
                                           reply_markup=sub_success_or_ban_inline)
        else:
            await message.bot.copy_message(chat_id=admin, from_chat_id=message.from_user.id,
                                           message_id=message.message_id,
                                           caption=f"💰 Подтвердите покупку.\n"
                                                   f"\nПользователь: @{message.from_user.username},"
                                                   f" <b>{message.from_user.first_name}</b>\n"
                                                   f"[ID:{message.from_user.id}]\nТариф: <b>Полгода</b>\nСумма к оплате: "
                                                   f"<b>550₽.</b>\nПлатежная система: <b>Перевод по номеру телефона</b>"
                                           , reply_markup=sub_success_or_ban_inline)
    await message.bot.send_message(message.from_user.id, '✅ Спасибо! Квитанция отправлена на проверку, вы получите '
                                                         'уведомление как только её проверят.')
    await state.finish()
    redis_pool = await connect_to_redis()
    user_data = {
        'first_name': message.from_user.first_name,
        'user_id': message.from_user.id,
        'username': message.from_user.username,
        'season': 'полгода',
        'exact_time': '180'
    }
    user_data_str = json.dumps(user_data)
    await redis_pool.set(name='user_data', value=user_data_str)


async def sub_success(call: CallbackQuery):
    redis_pool = await connect_to_redis()
    user_data_str = await redis_pool.get('user_data')
    user_data = json.loads(user_data_str)
    first_name_redis = user_data['first_name']
    username_redis = user_data['username']
    user_id = user_data['user_id']
    season = user_data['season']
    exact_time = user_data['exact_time']
    time_sub = int(time.time()) + days_to_seconds(int(exact_time))
    db.set_time_sub(user_id, time_sub)
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_message(user_id, f"Вам выдана подписка на {season}!\n"
                                         f"Вы получили приглашение в канал/чат 👇\n"
                                         f"<b>- ТРАНСФЕР-МОСТ Заказы</b>\n"
                                         f"Для перехода в главное меню, отправьте боту команду"
                                         f" - /start.", reply_markup=sub_link_inline)
    for admin in ADMIN_IDS:
        await call.bot.send_message(admin, f"💰 Новая подписка.\n"
                                           f"\nПользователь: @{username_redis}, <b>{first_name_redis}</b>\n"
                                           f"[ID:{user_id}] только что оформил подписку на {season}."
                                           f"\n\nСрок подписки: <b>{exact_time} дней.</b>")


async def sub_ban(call: CallbackQuery):
    redis_pool = await connect_to_redis()
    user_data_str = await redis_pool.get('user_data')
    user_data = json.loads(user_data_str)
    first_name_redis = user_data['first_name']
    username_redis = user_data['username']
    user_id = user_data['user_id']
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_message(user_id, '✖ Ваша квитанция была отклонена! Попробуйте заново, '
                                         'или обратитесь за помощью к админу!')
    await call.bot.send_message(call.from_user.id, f'✖ Квитанция пользователя @{username_redis},'
                                                   f' <b>{first_name_redis}</b> была отклонена!')


def register_card_pay(dp: Dispatcher):
    dp.register_callback_query_handler(
        sub_pay_month_card, IsBanFilter(),
        text='submonth',
        state="*",
    )
    dp.register_callback_query_handler(
        sub_pay_three_month_card, IsBanFilter(),
        text='subthreemonth',
        state='*'
    )
    dp.register_callback_query_handler(
        sub_pay_half_year_card, IsBanFilter(),
        text='subhalfyear',
        state='*'
    )
    dp.register_callback_query_handler(
        sub_pay_month_card_sure, IsBanFilter(),
        text='user_paid_month',
        state='*'
    )
    dp.register_message_handler(
        sub_pay_month_card_state, IsBanFilter(),
        state=SubPayCardState.pay_month,
        content_types=["text", "photo", "pinned_message"]
    )
    dp.register_callback_query_handler(
        sub_pay_three_month_card_sure, IsBanFilter(),
        text='user_paid_three_month',
        state='*'
    )
    dp.register_message_handler(
        sub_pay_three_month_card_state, IsBanFilter(),
        state=SubPayCardState.pay_three_month,
        content_types=["text", "photo", "pinned_message"]
    )
    dp.register_callback_query_handler(
        sub_pay_half_year_card_sure, IsBanFilter(),
        text='user_paid_half_year',
        state='*'
    )
    dp.register_message_handler(
        sub_pay_half_year_card_state, IsBanFilter(),
        state=SubPayCardState.pay_half_year,
        content_types=["text", "photo", "pinned_message"]
    )
    dp.register_callback_query_handler(
        sub_success, AdminFilter(),
        text='sub_success',
        state='*'
    )
    dp.register_callback_query_handler(
        sub_ban, AdminFilter(),
        text='sub_ban',
        state='*'
    )