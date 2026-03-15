"""Technical indicators for trading strategies."""
import numpy as np
from typing import List, Union
from loguru import logger

def calculate_sma(prices: List[float], window: int) -> List[float]:
    """
    Calculate Simple Moving Average.
    
    Args:
        prices: List of price values
        window: Moving average window size
        
    Returns:
        List of SMA values (first window-1 elements are NaN)
    """
    if len(prices) < window:
        logger.warning(f"Not enough data points ({len(prices)}) for SMA-{window}")
        return [np.nan] * len(prices)
    
    try:
        prices_array = np.array(prices, dtype=np.float64)
        sma = np.convolve(prices_array, np.ones(window), 'valid') / window
        
        # Pad with NaN at the beginning to maintain array length
        sma_padded = np.concatenate([np.full(window - 1, np.nan), sma])
        
        logger.debug(f"Calculated SMA-{window} with {len(sma)} valid values")
        return sma_padded.tolist()
        
    except Exception as e:
        logger.error(f"Error calculating SMA: {e}")
        return [np.nan] * len(prices)

def calculate_ema(prices: List[float], window: int) -> List[float]:
    """
    Calculate Exponential Moving Average.
    
    Args:
        prices: List of price values
        window: Moving average window size
        
    Returns:
        List of EMA values (first element is SMA for seed)
    """
    if len(prices) < window:
        logger.warning(f"Not enough data points ({len(prices)}) for EMA-{window}")
        return [np.nan] * len(prices)
    
    try:
        prices_array = np.array(prices, dtype=np.float64)
        
        # Calculate multiplier
        multiplier = 2 / (window + 1)
        
        # Initialize EMA array
        ema = np.zeros_like(prices_array)
        
        # First EMA value is SMA
        ema[:window - 1] = np.nan
        ema[window - 1] = np.mean(prices_array[:window])
        
        # Calculate EMA for remaining values
        for i in range(window, len(prices_array)):
            ema[i] = (prices_array[i] - ema[i-1]) * multiplier + ema[i-1]
        
        logger.debug(f"Calculated EMA-{window}")
        return ema.tolist()
        
    except Exception as e:
        logger.error(f"Error calculating EMA: {e}")
        return [np.nan] * len(prices)

def calculate_rsi(prices: List[float], window: int = 14) -> List[float]:
    """
    Calculate Relative Strength Index.
    
    Args:
        prices: List of price values
        window: RSI window size
        
    Returns:
        List of RSI values (first window elements are NaN)
    """
    if len(prices) < window + 1:
        logger.warning(f"Not enough data points ({len(prices)}) for RSI-{window}")
        return [np.nan] * len(prices)
    
    try:
        prices_array = np.array(prices, dtype=np.float64)
        
        # Calculate price changes
        deltas = np.diff(prices_array)
        
        # Separate gains and losses
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        # Calculate average gains and losses
        avg_gain = np.zeros_like(prices_array)
        avg_loss = np.zeros_like(prices_array)
        
        avg_gain[:window] = np.nan
        avg_loss[:window] = np.nan
        
        # First average
        avg_gain[window] = np.mean(gains[:window])
        avg_loss[window] = np.mean(losses[:window])
        
        # Subsequent averages
        for i in range(window + 1, len(prices_array)):
            avg_gain[i] = (avg_gain[i-1] * (window - 1) + gains[i-1]) / window
            avg_loss[i] = (avg_loss[i-1] * (window - 1) + losses[i-1]) / window
        
        # Calculate RS and RSI
        rs = avg_gain / np.where(avg_loss == 0, 0.001, avg_loss)  # Avoid division by zero
        rsi = 100 - (100 / (1 + rs))
        
        # Handle cases where avg_loss is 0 (RSI = 100)
        rsi[avg_loss == 0] = 100
        
        logger.debug(f"Calculated RSI-{window}")
        return rsi.tolist()
        
    except Exception as e:
        logger.error(f"Error calculating RSI: {e}")
        return [np.nan] * len(prices)
