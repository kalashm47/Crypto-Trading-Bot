"""Logging configuration for the bot."""
import sys
from loguru import logger

def setup_logger():
    """Configure loguru logger with custom format."""
    logger.remove()  # Remove default handler
    
    # Add console handler with custom format
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )
    
    # Add file handler for errors
    logger.add(
        "logs/bot_{time:YYYY-MM-DD}.log",
        rotation="500 MB",
        retention="10 days",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        backtrace=True,
        diagnose=True
    )
    
    # Add file handler for all logs
    logger.add(
        "logs/bot_{time:YYYY-MM-DD}.log",
        rotation="500 MB",
        retention="10 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    )
    
    return logger

# Create logs directory
import os
os.makedirs("logs", exist_ok=True)

__all__ = ["setup_logger"]
