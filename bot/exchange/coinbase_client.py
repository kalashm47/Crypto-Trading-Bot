"""Coinbase API client."""
import requests
from typing import Optional
from loguru import logger
from bot.config import config


class CoinbaseClient:

    def __init__(self):
        self.base_url = config.COINBASE_BASE_URL
        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "CryptoBot/1.0"
        })

    def get_ticker_price(self, symbol: Optional[str] = None) -> Optional[float]:

        symbol = symbol or config.SYMBOL

        try:
            endpoint = f"{self.base_url}/prices/{symbol}/spot"

            logger.debug(f"Fetching price for {symbol}")

            response = self.session.get(endpoint, timeout=10)
            response.raise_for_status()

            data = response.json()

            price = float(data["data"]["amount"])

            logger.info(f"{symbol} price: ${price:,.2f}")

            return price

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None

        except (KeyError, ValueError) as e:
            logger.error(f"Invalid response format: {e}")
            return None


coinbase_client = CoinbaseClient()