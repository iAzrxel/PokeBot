import os
from dotenv import load_dotenv

load_dotenv()

BOT_USERNAME = os.getenv("BOT_USERNAME")
BOT_PASSWORD = os.getenv("BOT_PASSWORD")
TARGET_USERNAME = os.getenv("TARGET_USERNAME")
BATTLE_FORMAT = os.getenv("BATTLE_FORMAT", "gen0randombattle")

def validate_config():
    required = {
        "BOT_USERNAME": BOT_USERNAME,
        "BOT_PASSWORD": BOT_PASSWORD,
        "TARGET_USERNAME": TARGET_USERNAME,
    }

    missing = [key for key, value in required.items() if not value]

    if missing:
        raise ValueError(f"Missing env variables: {', '.join(missing)}")