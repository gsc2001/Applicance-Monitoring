import os


DATABASE_URL = os.getenv('DATABASE_URL', None)
DATABASE_TOKEN = os.getenv('DATABASE_TOKEN', None)

ALLOWED_HOSTS = [
    "*"
]
XOR_KEY = "AB12:>"

org = "gurkiratsingh2001@gmail.com"
bucket = "esw"