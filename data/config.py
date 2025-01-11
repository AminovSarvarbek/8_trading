from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
DB_URL = env.str("DB_URL")
ADMINS = env.list("ADMINS")

API_KEY = env.str("API_KEY")
SECRET_KEY = env.str("SECRET_KEY")