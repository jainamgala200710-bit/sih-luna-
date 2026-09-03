"""
Logging utilities for LunaAlign AI.
Provides centralized logging configuration and helper functions.
"""

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Optional

def setup_logging(config=None, log_level=None, log_file=None):
    """
    Set up logging configuration for the application.
    
    Args:
        config: Configuration dictionary (optional)
        log_level: Logging level override (optional)
        log_file: Log file path override (optional)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Get configuration values if config provided
    if config is not None:
        log_config = config.get('logging', {})
        level_str = log_config.get('level', 'INFO')
        fmt = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        date_fmt = log_config.get('date_format', '%Y-%m-%d %H:%M:%S')
        file_enabled = log_config.get('file_enabled', True)
        file_path = log_config.get('file_path', 'logs/lunaalign.log')
        file_rotation = log_config.get('file_rotation', 'midnight')
        file_backup_count = log_config.get('file_backup_count', 30)
        console_enabled = log_config.get('console_enabled', True)
    else:
        # Default values
        level_str = 'INFO'
        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        date_fmt = '%Y-%m-%d %H:%M:%S'
        file_enabled = True
        file_path = 'logs/lunaalign.log'
        file_rotation = 'midnight'
        file_backup_count = 30
        console_enabled = True
    
    # Override if explicitly provided
    if log_level is not None:
        level_str = log_level
    if log_file is not None:
        file_path = log_file
    
    # Convert level string to logging constant
    numeric_level = getattr(logging, level_str.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level_str}')
    
    # Create formatter
    formatter = logging.Formatter(fmt, date_fmt)
    
    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(numeric_level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Add console handler if enabled
    if console_enabled:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # Add file handler if enabled
    if file_enabled:
        # Ensure log directory exists
        log_dir = os.path.dirname(file_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Set up timed rotating file handler
        file_handler = TimedRotatingFileHandler(
            file_path,
            when=file_rotation,
            backupCount=file_backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Log the startup
    logger.info(f"Logging initialized - Level: {level_str}, File: {file_path if file_enabled else 'None'}")
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (typically __name__)
    
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)

class LoggerMixin:
    """
    Mixin class to add logging capabilities to any class.
    """
    @property
    def logger(self):
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)
        return self._logger
