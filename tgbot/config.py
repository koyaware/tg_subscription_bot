import datetime
import time
from pathlib import Path

from environs import Env

from tgbot.db import Database

BASE_DIR = (Path(__file__).resolve()).parent


env = Env()
env.read_env('.env')

BOT_TOKEN = env.str('BOT_TOKEN')
PAYMENT_TOKEN = env.str('PAYMENT_TOKEN')

ADMIN_IDS = [2420239, ]

db = Database('database.db')


def days_to_seconds(days):
    return days * 24 * 60 * 60


def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now

    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        return dt