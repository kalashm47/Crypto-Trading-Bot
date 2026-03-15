"""Configuration management for the bot."""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:

    # Coinbase settings
    COINBASE_BASE_URL = os.getenv(
        "COINBASE_BASE_URL",
        "https://api.coinbase.com/v2"
    )

    SYMBOL = os.getenv(
        "TRADING_SYMBOL",
        "BTC-USD"
    )

    # Bot settings
    UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "60"))
    MAX_HISTORY = int(os.getenv("MAX_HISTORY", "100"))

    # Strategy parameters
    SMA_SHORT_WINDOW = int(os.getenv("SMA_SHORT_WINDOW", "10"))
    SMA_LONG_WINDOW = int(os.getenv("SMA_LONG_WINDOW", "30"))


config = Config()