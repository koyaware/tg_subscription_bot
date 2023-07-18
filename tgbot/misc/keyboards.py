from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.commands import Commands

btnProfile = KeyboardButton(Commands.my_profile.value)
btnSub = KeyboardButton(Commands.my_subs.value)
btnFeedback = KeyboardButton(Commands.feedback.value)
btnChat = KeyboardButton(Commands.chat.value)
btnAdmin = KeyboardButton(Commands.admin_menu.value)
btnRates = KeyboardButton(Commands.rates.value)
btnSpeaker = KeyboardButton(Commands.mailing.value)
btnComeBack = KeyboardButton(Commands.come_back.value)

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenuAdmin = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnProfile, btnSub)
mainMenu.add(btnFeedback)

mainMenuAdmin.add(btnProfile, btnSub)
mainMenuAdmin.add(btnFeedback)
mainMenuAdmin.add(btnChat)
mainMenuAdmin.add(btnAdmin)

adminMenu = ReplyKeyboardMarkup(resize_keyboard=True)
adminMenu.add(btnRates, btnSpeaker)
adminMenu.add(btnComeBack)

subMenu = ReplyKeyboardMarkup(resize_keyboard=True)
subMenu.add(btnProfile, btnSub)
subMenu.add(btnChat)
subMenu.add(btnFeedback)


sub_inline_markup = InlineKeyboardMarkup(row_width=1)

btnSubFree = InlineKeyboardButton(text="Пробный на 3 месяца", callback_data="subfree")
btnSubMonth = InlineKeyboardButton(text="Месяц - 300₽", callback_data="submonthmenu")
btnSubHalfYear = InlineKeyboardButton(text="Полгода - 600₽", callback_data="subhalfyearmenu")

sub_inline_markup.insert(btnSubFree)
sub_inline_markup.insert(btnSubMonth)
sub_inline_markup.insert(btnSubHalfYear)

main_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('🖥️ Наш сайт', callback_data='site', url='https://xn----7sbp3acjidhfbkt.xn--p1ai/'),
     InlineKeyboardButton('📱 Страница ВК', callback_data='vk', url='https://vk.com/transfermost')]
])

cancel_inline = InlineKeyboardMarkup()
cancel_inline.insert(InlineKeyboardButton(text='❌ Отмена', callback_data='cancelbutton'))

feedback_inline = InlineKeyboardMarkup(row_width=1)

btnBanInline = InlineKeyboardButton(text="🚫 Забанить пользователя", callback_data='ban_user')
btnFeedbackInline = InlineKeyboardButton(text="📨 Ответить", callback_data='feedback_user')

feedback_inline.insert(btnFeedbackInline)
feedback_inline.insert(btnBanInline)

rates_inline = InlineKeyboardMarkup(row_width=1)

btnBanIDInline = InlineKeyboardButton(text="🚫 Забанить пользователя", callback_data='ban_user_id')
btnUnBanInline = InlineKeyboardButton(text="🔥 Разбанить пользователя", callback_data='unban_user')
btnUserBannedInline = InlineKeyboardButton(text="📋 Таблица заблокированных", callback_data='banned_user')

rates_inline.insert(btnBanIDInline)
rates_inline.insert(btnUnBanInline)
rates_inline.insert(btnUserBannedInline)

mailing_inline = InlineKeyboardMarkup(row_width=1)

btnSendAll = InlineKeyboardButton(text="📟 Отправить всем пользователям", callback_data='send_all')
btnSendSub = InlineKeyboardButton(text="📥 Отправить только подписчикам", callback_data='send_sub')
btnSendNotSub = InlineKeyboardButton(text="📤 Отправить только людям без подписки", callback_data='send_not_sub')

mailing_inline.insert(btnSendAll)
mailing_inline.insert(btnSendSub)
mailing_inline.insert(btnSendNotSub)

submonthmenu_inline = InlineKeyboardMarkup(row_width=1)

btnPayMonth = InlineKeyboardButton(text="💳 Оплатить", callback_data='submonth')
btnPromoCode = InlineKeyboardButton(text="🎁 Ввести промокод", callback_data='promocode')

submonthmenu_inline.insert(btnPayMonth)
submonthmenu_inline.insert(btnPromoCode)

subhalfyear_inline = InlineKeyboardMarkup(row_width=1)

btnPayHalfYear = InlineKeyboardButton(text='💳 Оплатить', callback_data='subhalfyear')

subhalfyear_inline.insert(btnPayHalfYear)
subhalfyear_inline.insert(btnPromoCode)