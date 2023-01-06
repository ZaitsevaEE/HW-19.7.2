#
# valid_email = "vasya@mail.com"
# valid_password = "12345"

import os

from dotenv import load_dotenv

load_dotenv()

valid_email = os.getenv('valid_email')
valid_password = os.getenv('valid_password')

invalid_email = 'yolka@mail.ru'
invalid_password = '123456'
