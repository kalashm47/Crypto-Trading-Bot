"""Technical indicators for trading strategies."""

import numpy as np
from typing import Sequence, List
from loguru import logger


def calculate_sma(prices: Sequence[float], window: int) -> List[float]:
    """
    Calculate Simple Moving Average.
    """

    prices = list(prices)

    if len(prices) < window:
        logger.warning(f"Not enough data points ({len(prices)}) for SMA-{window}")
        return [np.nan] * len(prices)

    try:
        prices_array = np.array(prices, dtype=np.float64)

        sma = np.convolve(prices_array, np.ones(window), "valid") / window

        sma_padded = np.concatenate(
            [np.full(window - 1, np.nan), sma]
        )

        logger.debug(f"Calculated SMA-{window}")

        return sma_padded.tolist()

    except Exception as e:

        logger.error(f"SMA calculation error: {e}")

        return [np.nan] * len(prices)


def calculate_ema(prices: Sequence[float], window: int) -> List[float]:
    """
    Calculate Exponential Moving Average.
    """

    prices = list(prices)

    if len(prices) < window:
        logger.warning(f"Not enough data points ({len(prices)}) for EMA-{window}")
        return [np.nan] * len(prices)

    try:

        prices_array = np.array(prices, dtype=np.float64)

        multiplier = 2 / (window + 1)

        ema = np.zeros_like(prices_array)

        ema[: window - 1] = np.nan

        ema[window - 1] = np.mean(prices_array[:window])

        for i in range(window, len(prices_array)):

            ema[i] = (
                prices_array[i] - ema[i - 1]
            ) * multiplier + ema[i - 1]

        logger.debug(f"Calculated EMA-{window}")

        return ema.tolist()

    except Exception as e:

        logger.error(f"EMA calculation error: {e}")

        return [np.nan] * len(prices)


def calculate_rsi(prices: Sequence[float], window: int = 14) -> List[float]:
    """
    Calculate Relative Strength Index.
    """

    prices = list(prices)

    if len(prices) < window + 1:
        logger.warning(f"Not enough data points ({len(prices)}) for RSI-{window}")
        return [np.nan] * len(prices)

    try:

        prices_array = np.array(prices, dtype=np.float64)

        deltas = np.diff(prices_array)

        gains = np.where(deltas > 0, deltas, 0)

        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.zeros_like(prices_array)
        avg_loss = np.zeros_like(prices_array)

        avg_gain[:window] = np.nan
        avg_loss[:window] = np.nan

        avg_gain[window] = np.mean(gains[:window])
        avg_loss[window] = np.mean(losses[:window])

        for i in range(window + 1, len(prices_array)):

            avg_gain[i] = (
                avg_gain[i - 1] * (window - 1) + gains[i - 1]
            ) / window

            avg_loss[i] = (
                avg_loss[i - 1] * (window - 1) + losses[i - 1]
            ) / window

        rs = avg_gain / np.where(avg_loss == 0, 0.001, avg_loss)

        rsi = 100 - (100 / (1 + rs))

        rsi[avg_loss == 0] = 100

        logger.debug(f"Calculated RSI-{window}")

        return rsi.tolist()

    except Exception as e:

        logger.error(f"RSI calculation error: {e}")

        return [np.nan] * len(prices)