#Copyright @ISmartCoder
#Updates Channel https://t.me/TheSmartDev
import os
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json

load_dotenv()

def get_env_or_default(key, default=None, cast_func=str):
    value = os.getenv(key)
    if value is not None and value.strip() != "":
        try:
            return cast_func(value)
        except (ValueError, TypeError) as e:
            print(f"Error casting {key} with value '{value}' to {cast_func.__name__}: {e}")
            return default
    return default

# ✅ Your Credentials
API_ID = get_env_or_default("API_ID", "26359571", cast_func=int)
API_HASH = get_env_or_default("API_HASH", "9d014339150e1ed7d44b30333bd2a836")
BOT_TOKEN = get_env_or_default("BOT_TOKEN", "8384242428:AAGNFnG4SPgPRbkoMzNDTemLZl7OdXhZ8jw")
DEVELOPER_ID = get_env_or_default("DEVELOPER_ID", "7971284841", cast_func=int)
UPDATE_CHANNEL_URL = get_env_or_default("UPDATE_CHANNEL_URL", "https://t.me/VirusX_Public")
ADMIN_IDS = get_env_or_default("ADMIN_IDS", "7971284841", cast_func=str)
COMMAND_PREFIX = get_env_or_default("COMMAND_PREFIX", ".,/,!,#", cast_func=str).split(",")

# ✅ MongoDB Atlas Connection (আপনার আসল URL)
MONGO_URL = get_env_or_default("MONGO_URL", 
    "mongodb+srv://TwilioBot:BotPassword123@cluster0.dameuvg.mongodb.net/twiliobot?retryWrites=true&w=majority&appName=Cluster0"
)

# ✅ Required Channels
REQUIRED_CHANNELS = [
    {"username": "@cybersentinelbangladesh", "id": -1002353396382},
    {"username": "@VirusX_Public", "id": -1003171221510}
]

ADMIN_IDS = [int(x.strip()) for x in ADMIN_IDS.split(",") if x.strip().isdigit()]

required_vars = {
    "API_ID": API_ID,
    "API_HASH": API_HASH,
    "BOT_TOKEN": BOT_TOKEN,
    "DEVELOPER_ID": DEVELOPER_ID,
    "UPDATE_CHANNEL_URL": UPDATE_CHANNEL_URL,
    "MONGO_URL": MONGO_URL,
}

for var_name, var_value in required_vars.items():
    if var_value is None or var_value == f"Your_{var_name}_Here" or (isinstance(var_value, str) and var_value.strip() == ""):
        raise ValueError(f"Required variable {var_name} is missing or invalid. Set it in .env (VPS), config.py (VPS), or Heroku config vars.")

print("✅ Config loaded successfully!")
print(f"📝 COMMAND_PREFIX: {COMMAND_PREFIX}")
print(f"👑 ADMIN_IDS: {ADMIN_IDS}")
print(f"🗄️ MONGO_URL: {MONGO_URL}")

# Rest of your channel subscription code...
async def check_channel_subscription(user_id, app: Client):
    not_joined = []
    for channel in REQUIRED_CHANNELS:
        try:
            if channel.get("username"):
                member = await app.get_chat_member(channel["username"], user_id)
                if member.status in ["left", "kicked", "banned"]:
                    not_joined.append(channel["username"])
        except Exception as e:
            print(f"Error checking {channel['username']}: {e}")
    return not_joined

# ... (বাকি functions)