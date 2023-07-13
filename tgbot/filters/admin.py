import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import ADMIN_IDS


class AdminFilter(BoundFilter):
    key = 'is_superuser'

    def __init__(self, is_superuser: typing.Optional[bool] = None):
        self.is_superuser = is_superuser

    async def check(self, obj):
        if self.is_superuser is None:
            return False
        return (obj.from_user.id in ADMIN_IDS) == self.is_superuser