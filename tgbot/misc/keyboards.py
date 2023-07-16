from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.commands import Commands

btnProfile = KeyboardButton(Commands.my_profile.value)
btnSub = KeyboardButton(Commands.my_subs.value)
btnFeedback = KeyboardButton(Commands.feedback.value)
btnChat = KeyboardButton(Commands.chat.value)
btnAdmin = KeyboardButton(Commands.admin_menu.value)
btnRates = KeyboardButton(Commands.rates.value)
btnSpeaker = KeyboardButton(Commands.mailing.value)

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenuAdmin = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnProfile, btnSub)
mainMenu.add(btnFeedback)
mainMenuAdmin.add(btnProfile, btnSub)
mainMenuAdmin.add(btnFeedback)
mainMenuAdmin.add(btnAdmin)

adminMenu = ReplyKeyboardMarkup(resize_keyboard=True)
adminMenu.add(btnRates, btnSpeaker)


sub_inline_markup = InlineKeyboardMarkup(row_width=1)

btnSubFree = InlineKeyboardButton(text="Пробный на 3 месяца", callback_data="subfree")
btnSubMonth = InlineKeyboardButton(text="Месяц - 300₽", callback_data="submonth")
btnSubHalfYear = InlineKeyboardButton(text="Полгода - 600₽", callback_data="subhalfyear")

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