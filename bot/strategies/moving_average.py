"""Moving average crossover strategy."""
from typing import Dict, List, Optional, Tuple
from loguru import logger
from bot.config import config
from bot.utils.indicators import calculate_sma

class MovingAverageStrategy:
    """Simple moving average crossover strategy."""
    
    def __init__(self, short_window: int = None, long_window: int = None):
        """
        Initialize strategy with configurable windows.
        
        Args:
            short_window: Short-term MA window
            long_window: Long-term MA window
        """
        self.short_window = short_window or config.SMA_SHORT_WINDOW
        self.long_window = long_window or config.SMA_LONG_WINDOW
        self.prices: List[float] = []
        self.signals: List[Dict] = []
        self.position = None  # None, 'long', 'short'
        
        logger.info(f"Initialized MA strategy: {self.short_window}/{self.long_window}")
    
    def update_price(self, price: float) -> None:
        """
        Add new price to history.
        
        Args:
            price: Current price
        """
        self.prices.append(price)
        
        # Keep only last N prices for performance
        if len(self.prices) > config.MAX_HISTORY:
            self.prices = self.prices[-config.MAX_HISTORY:]
        
        logger.debug(f"Added price ${price:,.2f} to history (total: {len(self.prices)})")
    
    def calculate_signals(self) -> Optional[Dict]:
        """
        Generate trading signals based on MA crossover.
        
        Returns:
            Signal dictionary or None if no signal
        """
        if len(self.prices) < self.long_window:
            logger.debug(f"Not enough data for signals ({len(self.prices)} < {self.long_window})")
            return None
        
        # Calculate moving averages
        sma_short = calculate_sma(self.prices, self.short_window)
        sma_long = calculate_sma(self.prices, self.long_window)
        
        # Get current and previous values
        current_short = sma_short[-1]
        current_long = sma_long[-1]
        
        if np.isnan(current_short) or np.isnan(current_long):
            logger.debug("MA values not available yet")
            return None
        
        # Check for crossover
        previous_short = sma_short[-2] if len(sma_short) > 1 and not np.isnan(sma_short[-2]) else current_short
        previous_long = sma_long[-2] if len(sma_long) > 1 and not np.isnan(sma_long[-2]) else current_long
        
        signal = None
        
        # Golden cross (short crosses above long)
        if previous_short <= previous_long and current_short > current_long:
            signal = {
                'type': 'BUY',
                'price': self.prices[-1],
                'short_ma': current_short,
                'long_ma': current_long,
                'timestamp': time.time(),
                'reason': 'Golden cross (MA crossover up)'
            }
            logger.success(f"BUY signal generated at ${self.prices[-1]:,.2f}")
        
        # Death cross (short crosses below long)
        elif previous_short >= previous_long and current_short < current_long:
            signal = {
                'type': 'SELL',
                'price': self.prices[-1],
                'short_ma': current_short,
                'long_ma': current_long,
                'timestamp': time.time(),
                'reason': 'Death cross (MA crossover down)'
            }
            logger.warning(f"SELL signal generated at ${self.prices[-1]:,.2f}")
        
        if signal:
            self.signals.append(signal)
            return signal
        
        return None
    
    def get_status(self) -> Dict:
        """
        Get current strategy status.
        
        Returns:
            Dictionary with current indicators and position
        """
        if len(self.prices) < self.long_window:
            return {'status': 'initializing', 'data_points': len(self.prices)}
        
        sma_short = calculate_sma(self.prices, self.short_window)
        sma_long = calculate_sma(self.prices, self.long_window)
        
        return {
            'status': 'running',
            'current_price': self.prices[-1] if self.prices else None,
            f'sma_{self.short_window}': sma_short[-1] if not np.isnan(sma_short[-1]) else None,
            f'sma_{self.long_window}': sma_long[-1] if not np.isnan(sma_long[-1]) else None,
            'position': self.position,
            'signals_generated': len(self.signals),
            'data_points': len(self.prices)
        }

# Import for timestamp
import time
import numpy as np
