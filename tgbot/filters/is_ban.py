import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import db


class IsBanFilter(BoundFilter):
    key = 'is_ban'

    def __init__(self, is_ban: typing.Optional[bool] = None):
        self.is_ban = is_ban

    async def check(self, obj):
        if db.get_ban_status(obj.from_user.id) is False:
            return True
        return False