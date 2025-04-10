import logging
import sys

from app.core.config import settings


def setup_logging() -> None:
    """
    Configure logging for the application.
    Sets up console and file handlers with the specified format.
    """
    # Create logger
    logger = logging.getLogger("restaurant_booking")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Remove existing handlers to avoid duplicates
    logger.handlers = []

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    console_formatter = logging.Formatter(settings.LOG_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create file handler
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    file_formatter = logging.Formatter(settings.LOG_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: The name of the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(f"restaurant_booking.{name}")


# Initialize logging when module is imported
setup_logging() 