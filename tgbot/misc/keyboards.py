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
btnAdminSub = KeyboardButton(Commands.admin_sub.value)
btnPromocodeMenu = KeyboardButton(Commands.promocode_menu.value)

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenuAdmin = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnSub, btnProfile)
mainMenu.add(btnFeedback)

mainMenuAdmin.add(btnSub, btnProfile)
mainMenuAdmin.add(btnFeedback)
mainMenuAdmin.add(btnChat)
mainMenuAdmin.add(btnAdmin)

adminMenu = ReplyKeyboardMarkup(resize_keyboard=True)
adminMenu.add(btnRates, btnSpeaker)
adminMenu.add(btnAdminSub, btnPromocodeMenu)
adminMenu.add(btnComeBack)

subMenu = ReplyKeyboardMarkup(resize_keyboard=True)
subMenu.add(btnSub, btnProfile)
subMenu.add(btnChat)
subMenu.add(btnFeedback)


sub_inline_markup = InlineKeyboardMarkup(row_width=1)

btnSubFree = InlineKeyboardButton(text="Пробный 14 дней - 0 ₽", callback_data="subfreemenu")
btnSubWeek = InlineKeyboardButton(text="Неделя - 150 ₽", callback_data="subweekmenu")
btnSubMonth = InlineKeyboardButton(text="Месяц - 150 ₽", callback_data="submonthmenu")
btnSubThreeMonth = InlineKeyboardButton(text="3 месяца - 300 ₽", callback_data="subthreemonthmenu")
btnSubHalfYear = InlineKeyboardButton(text="Полгода - 550 ₽", callback_data="subhalfyearmenu")

sub_inline_markup.insert(btnSubFree)
# sub_inline_markup.insert(btnSubWeek)
sub_inline_markup.insert(btnSubMonth)
sub_inline_markup.insert(btnSubThreeMonth)
sub_inline_markup.insert(btnSubHalfYear)

main_info = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('🖥️ Наш сайт', callback_data='site', url='https://xn----7sbp3acjidhfbkt.xn--p1ai/'),
     InlineKeyboardButton('📱 Страница ВК', callback_data='vk', url='https://vk.com/transfermost')]
])

sub_link_inline = InlineKeyboardMarkup(row_width=1)

btnSubLink = InlineKeyboardButton('🔗 Ссылки для доступа', callback_data='sublink')

sub_link_inline.insert(btnSubLink)

sub_link_private_inline = InlineKeyboardMarkup(row_width=1)

btnSubPrivateLink = InlineKeyboardButton('👉ТРАНСФЕР-МОСТ Заказы👈', callback_data='subprivatelink')

sub_link_private_inline.insert(btnSubPrivateLink)

sub_link_open_inline = InlineKeyboardMarkup(row_width=1)

btnSubOpenLink = InlineKeyboardButton('👉ВСТУПИТЬ👈', url='https://t.me/+VHuzPV-cvZlkZWQy', callback_data='subopenlink')

sub_link_open_inline.insert(btnSubOpenLink)

cancel_inline = InlineKeyboardMarkup()

btnCancel = InlineKeyboardButton(text='❌ Отмена', callback_data='cancelbutton')

cancel_inline.insert(btnCancel)

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

subweekmenu_inline = InlineKeyboardMarkup(row_width=1)

btnPayWeek = InlineKeyboardButton(text="💳 Оплатить", callback_data='subweek')
btnPromoCode = InlineKeyboardButton(text="🎁 Ввести промокод", callback_data='promocode')

subweekmenu_inline.insert(btnPayWeek)
subweekmenu_inline.insert(btnPromoCode)

submonthmenu_inline = InlineKeyboardMarkup(row_width=1)

btnPayMonth = InlineKeyboardButton(text="💳 Оплатить", callback_data='submonth')

submonthmenu_inline.insert(btnPayMonth)
submonthmenu_inline.insert(btnPromoCode)

subthreemonthmenu_inline = InlineKeyboardMarkup(row_width=1)

btnPayThreeMonth = InlineKeyboardButton(text="💳 Оплатить", callback_data='subthreemonth')

subthreemonthmenu_inline.insert(btnPayThreeMonth)
subthreemonthmenu_inline.insert(btnPromoCode)

subhalfyear_inline = InlineKeyboardMarkup(row_width=1)

btnPayHalfYear = InlineKeyboardButton(text='💳 Оплатить', callback_data='subhalfyear')

subhalfyear_inline.insert(btnPayHalfYear)
subhalfyear_inline.insert(btnPromoCode)

subfreemenu_inline = InlineKeyboardMarkup(row_width=1)

btnPayFree = InlineKeyboardButton(text="🆓 Активировать", callback_data='subfree')

subfreemenu_inline.insert(btnPayFree)
subfreemenu_inline.insert(btnPromoCode)

admin_sub_gift_inline = InlineKeyboardMarkup(row_width=1)

btnGiftWeek = InlineKeyboardButton(text="📦 Выдать на неделю", callback_data='giftweek')
btnGiftMonth = InlineKeyboardButton(text="📦 Выдать на месяц", callback_data='giftmonth')
btnGiftThreeMonth = InlineKeyboardButton(text="🎀 Выдать на 3 месяца", callback_data='giftthreemonth')
btnGiftHalfYear = InlineKeyboardButton(text="🎁 Выдать на полгода", callback_data='gifthalfyear')

# admin_sub_gift_inline.insert(btnGiftWeek)
admin_sub_gift_inline.insert(btnGiftMonth)
admin_sub_gift_inline.insert(btnGiftThreeMonth)
admin_sub_gift_inline.insert(btnGiftHalfYear)

promocode_menu_inline = InlineKeyboardMarkup(row_width=1)

btnAddPromocode = InlineKeyboardButton(text="💘 Добавить промокод", callback_data='add_promocode')
btnAllPromocodes = InlineKeyboardButton(text="💞 Все промокоды", callback_data='all_promocodes')
btnDeletePromocode = InlineKeyboardButton(text="💔 Удалить промокод", callback_data='delete_promocode')

promocode_menu_inline.insert(btnAddPromocode)
promocode_menu_inline.insert(btnDeletePromocode)
promocode_menu_inline.insert(btnAllPromocodes)

sub_pay_month_card_inline = InlineKeyboardMarkup(row_width=1)
sub_pay_three_month_card_inline = InlineKeyboardMarkup(row_width=1)
sub_pay_half_year_card_inline = InlineKeyboardMarkup(row_width=1)

btnUserPaid = InlineKeyboardButton(text='✅ Я оплатил', callback_data='user_paid_month')
btnUserPaidTheeMonth = InlineKeyboardButton(text='✅ Я оплатил', callback_data='user_paid_three_month')
btnUserPaidHalfYear = InlineKeyboardButton(text='✅ Я оплатил', callback_data='user_paid_half_year')

sub_pay_month_card_inline.insert(btnUserPaid)
sub_pay_month_card_inline.insert(btnCancel)

sub_pay_three_month_card_inline.insert(btnUserPaidTheeMonth)
sub_pay_three_month_card_inline.insert(btnCancel)

sub_pay_half_year_card_inline.insert(btnUserPaidHalfYear)
sub_pay_half_year_card_inline.insert(btnCancel)

sub_pay_card_sure_inline = InlineKeyboardMarkup(row_width=1)

sub_pay_card_sure_inline.insert(btnCancel)

sub_success_or_ban_inline = InlineKeyboardMarkup()

btnSubSuccess = InlineKeyboardButton(text='✅ Подтвердить', callback_data='sub_success')
btnSubBan = InlineKeyboardButton(text='✖ Спам', callback_data='sub_ban')

sub_success_or_ban_inline.insert(btnSubSuccess)
sub_success_or_ban_inline.insert(btnSubBan)
