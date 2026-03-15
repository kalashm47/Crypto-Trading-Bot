#!/usr/bin/env python3
"""Main entry point for the crypto trading bot."""

import time
import sys
import signal
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.logger import setup_logger
from bot.config import config
from bot.exchange.coinbase_client import coinbase_client
from bot.strategies.moving_average import MovingAverageStrategy
from loguru import logger


running = True


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    global running
    logger.info("Shutdown signal received...")
    running = False


def main_loop(strategy: MovingAverageStrategy):

    global running

    update_interval = config.UPDATE_INTERVAL

    logger.info(f"Starting main loop ({update_interval}s interval)")

    while running:

        try:

            price = coinbase_client.get_ticker_price()

            if price is not None:

                strategy.update_price(price)

                signal_data = strategy.calculate_signals()

                if signal_data:

                    logger.info(
                        f"SIGNAL {signal_data['type']} | "
                        f"price ${signal_data['price']:,.2f} | "
                        f"{signal_data['reason']}"
                    )

                if len(strategy.prices) % 10 == 0:

                    status = strategy.get_status()

                    logger.info(f"STATUS {status}")

            time.sleep(update_interval)

        except Exception as e:

            logger.error(f"Main loop error: {e}")

            time.sleep(5)


def main():

    setup_logger()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("=" * 50)
    logger.info("CRYPTO TRADING BOT STARTING")
    logger.info(f"Symbol: {config.SYMBOL}")
    logger.info(f"Update interval: {config.UPDATE_INTERVAL}s")
    logger.info(
        f"Strategy: MA({config.SMA_SHORT_WINDOW},{config.SMA_LONG_WINDOW})"
    )
    logger.info("=" * 50)

    strategy = MovingAverageStrategy(
        short_window=config.SMA_SHORT_WINDOW,
        long_window=config.SMA_LONG_WINDOW
    )

    logger.info("Starting price monitoring...")

    try:

        main_loop(strategy)

    except KeyboardInterrupt:

        logger.info("Keyboard interrupt")

    finally:

        logger.info("Bot shutdown complete")
        logger.info(f"Signals generated: {len(strategy.signals)}")


if __name__ == "__main__":
    main()