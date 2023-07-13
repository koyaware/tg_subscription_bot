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