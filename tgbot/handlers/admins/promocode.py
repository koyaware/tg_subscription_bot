import re
import time

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.config import db, days_to_seconds, connect_to_redis, ADMIN_IDS
from tgbot.filters import AdminFilter
from tgbot.filters.is_ban import IsBanFilter
from tgbot.misc.keyboards import cancel_inline
from tgbot.misc.states import PromoCodeState


async def promocode(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, 'Отправьте боту ваш промокод для скидки: ',
                                reply_markup=cancel_inline)
    await PromoCodeState.code.set()


async def promocode_state(message: Message, state: FSMContext):
    if not db.is_promo_code_used(message.from_user.id, message.text):
        discount = db.get_discount(message.text)
        if discount is not None:
            max_usage = db.apply_promocode(message.text)
            if max_usage is not None:
                db.mark_promo_code_as_used(message.from_user.id, message.text)
                time_sub = int(time.time()) + days_to_seconds(int(discount))
                db.set_time_sub(message.from_user.id, time_sub)
                await message.bot.send_message(message.from_user.id, f'Вы активировали промокод на {int(discount)} дней.')
                for admin in ADMIN_IDS:
                    await message.bot.send_message(admin, f"📇 Пользователь активировал промокод"
                                                          f"\n\nПользователь: @{message.from_user.username}, <b>{message.from_user.first_name}</b>\n"
                                                          f"[ID:{message.from_user.id}] только что активировал промокод на {int(discount)} дней.")
                await state.finish()
            else:
                await message.bot.send_message(message.from_user.id, 'Возможность использовать данный промокод исчерпан.')
                await state.finish()
        else:
            await message.bot.send_message(message.from_user.id, 'Произошла discount ошибка!')
            await state.finish()
    else:
        await message.bot.send_message(message.from_user.id, 'Такого промокода не существует или вы его уже активировали.')
        await state.finish()


async def add_promocode(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, 'Отправьте боту название вашего промокода для скидки:'
                                                         ' \n\nПример: NEW123',
                                   reply_markup=cancel_inline)
    await PromoCodeState.add_name.set()


async def add_promocode_state(message: Message, state: FSMContext):
    redis_pool = await connect_to_redis()
    await redis_pool.set(name='code_name', value=message.text)
    await message.bot.send_message(message.from_user.id, 'Отлично! Отправьте боту количество дней для вашего промокода: '
                                                         '\n\nПример: 7')
    await state.finish()
    await PromoCodeState.add_discount.set()


async def add_discount_state(message: Message, state: FSMContext):
    if message.text.isdecimal():
        redis_pool = await connect_to_redis()
        await redis_pool.set(name='code_discount', value=message.text)
        await message.bot.send_message(message.from_user.id, 'Отлично! Отправьте боту максимальное количество'
                                                             ' использований для вашего промокода: '
                                                             '\n\nПример: 10')
        await state.finish()
        await PromoCodeState.add_max_usage.set()
    else:
        await message.bot.send_message(message.from_user.id, 'Ответ должнен быть числом. Попробуйте заново!')
        await state.finish()


async def add_max_usage_state(message: Message, state: FSMContext):
    if message.text.isdecimal():
        redis_pool = await connect_to_redis()
        promo_code = await redis_pool.get(name='code_name')
        code_name = str(promo_code).replace("b'", "").replace("'", "")
        discount = await redis_pool.get(name='code_discount')
        code_discount = re.sub(r'\D', '', discount.decode())
        try:
            db.add_promocode(code_name, int(code_discount), int(message.text))
            await message.bot.send_message(message.from_user.id, f'Отлично!\nВаш промокод: <b>{code_name}</b>'
                                                                 f'\nКоличество Дней: <b>{code_discount}</b>'
                                                                 f'\nМаксимальное количество использований: <b>{message.text}</b>')
            await state.finish()
        except Exception as e:
            await message.bot.send_message(message.from_user.id, 'Такой промокод уже существует!')
            return await state.finish()
    else:
        await message.bot.send_message(message.from_user.id, 'Ответ должнен быть числом. Попробуйте заново!')
        await state.finish()


async def delete_promocode(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, 'Отправьте боту название вашего промокода для удаления:'
                                                         ' \n\nПример: NEW123',
                                   reply_markup=cancel_inline)
    await PromoCodeState.delete.set()


async def delete_promocode_state(message: Message, state: FSMContext):
    all_promocodes = db.get_all_promocodes()
    if str(message.text) not in all_promocodes:
        await message.bot.send_message(message.from_user.id, 'Такого промокода не существует!')
        return await state.finish()
    db.delete_promocode(str(message.text))
    await message.bot.send_message(message.from_user.id, f'Отлично! Вы удалили промокод <b>{message.text}</b>')
    await state.finish()


async def all_promocodes(call: CallbackQuery):
    all_promocodes = db.get_all_promocodes_each()
    if not all_promocodes:
        return await call.bot.send_message(call.from_user.id, "<b>Нет зарегестрированных промокодов.</b>")
    else:
        for promocode in all_promocodes:
            formatted_promocode_1 = f"Промокод: <b>{promocode[0]}</b>"
            formatted_promocode_2 = f"Количество дней: <b>{promocode[1]}</b>"
            formatted_promocode_3 = f"Количество использований: <b>{promocode[2]}</b>"
            await call.bot.send_message(call.from_user.id, f'{formatted_promocode_1}\n{formatted_promocode_2}'
                                                           f'\n{formatted_promocode_3}\n')


def register_promocode(dp: Dispatcher):
    dp.register_callback_query_handler(
        promocode, IsBanFilter(), text='promocode', state='*'
    )
    dp.register_message_handler(
        promocode_state, IsBanFilter(), state=PromoCodeState.code
    )
    dp.register_callback_query_handler(
        add_promocode, AdminFilter(), text='add_promocode',
        state='*'
    )
    dp.register_message_handler(
        add_promocode_state, AdminFilter(),
        state=PromoCodeState.add_name
    )
    dp.register_message_handler(
        add_discount_state, AdminFilter(),
        state=PromoCodeState.add_discount
    )
    dp.register_message_handler(
        add_max_usage_state, AdminFilter(),
        state=PromoCodeState.add_max_usage
    )
    dp.register_callback_query_handler(
        delete_promocode, AdminFilter(), text='delete_promocode',
        state='*'
    )
    dp.register_message_handler(
        delete_promocode_state, AdminFilter(),
        state=PromoCodeState.delete
    )
    dp.register_callback_query_handler(
        all_promocodes, AdminFilter(), text='all_promocodes',
        state='*'
    )