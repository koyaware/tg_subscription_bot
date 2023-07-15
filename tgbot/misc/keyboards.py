from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


btnProfile = KeyboardButton('💻 Мои подписки')
btnSub = KeyboardButton('❤ Тарифы')
btnFeedback = KeyboardButton('📨 Обратная связь')
btnChat = KeyboardButton('📨 Чат')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnProfile, btnSub)
mainMenu.add(btnFeedback)


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