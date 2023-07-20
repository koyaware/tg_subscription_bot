from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from tgbot.filters.is_ban import IsBanFilter
from tgbot.misc.keyboards import sub_pay_card_sure_inline, sub_pay_card_inline
from tgbot.misc.states import SubPayCardState


async def sub_pay_month_card(call: CallbackQuery):
    await call.message.bot.send_message(call.from_user.id, 'Тариф: <b>Месяц</b>\nСпособ оплаты:'
                                                           ' <b>Перевод по номеру телефона</b>\nСумма к отплате: 150₽.'
                                                           '\nИнформация об оплате:\nТинков <code>89124436363</code>'
                                                           '\nСкрин чека отправить админу, либо сюда же в бота',
                                        reply_markup=sub_pay_card_inline)
    await SubPayCardState.pay.set()


async def sub_pay_month_card_state(message: Message):
    await message.bot.edit_message_text('💰 <b>Оплатили?</b>\n\nОтправьте боту квинтацию об '
                                                              'оплате:\n<b>скриншот или фото</b>\n'
                                                              'На квинтации должны быть четко видны:\n<b>'
                                                              'дата, время и сумма платежа.</b>\n'
                                                              'Или вы можете отправить точную дату и время платежа',
                                        message.chat.id, message.message_id,
                                        reply_markup=sub_pay_card_sure_inline)


def register_card_pay(dp: Dispatcher):
    dp.register_callback_query_handler(
        sub_pay_month_card, IsBanFilter(),
        text='Сюда ввод submonth по идее',
        state="*",
    )
    dp.register_message_handler(
        sub_pay_month_card_state, IsBanFilter(),
        state=SubPayCardState.pay
    )