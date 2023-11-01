from dotenv import load_dotenv
from decouple import config


load_dotenv()

BOT_TOKEN = config('BOT_TOKEN', default='')

FLOOD_TIME = config('FLOOD_TIME', cast=int, default=15)
EXCEPT_USERS = config(
    'EXCEPT_USERS',
    default='',
    cast=lambda v: [int(i) for i in filter(str.isdigit, (s.strip() for s in v.split(',')))]
)

SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL', default='sqlite:///db.sqlite3')
