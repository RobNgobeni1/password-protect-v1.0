import os 
import logging 
from logging.handlers import RotatingFileHandler 
from pathlib import Path 
from dotenv import load_dotenv
from datetime import datetime as dt
 
def setup_logger(name : str = __name__) -> logging.Logger: 
    """ 
    Create or retrieve a configured logger. 
    Creates a rotating file handler and console handler with appropriate 
    formatting and log levels. 

    Args: 
        name: Logger name (use __name__ from calling module for best practice) 

    Returns: 
        logging.Logger: Configured logger instance 
    """ 
    logger = logging.getLogger(name) 
    today : str = dt.now().strftime("%d%m%Y")

    # Prevent duplicate handlers if setup_logger called multiple times 
    if logger.handlers: 
        return logger 

    # Load environment variables 
    load_dotenv() 

    default_directory = os.getenv("MAIN_DIRECTORY") 

    if not default_directory: 
        raise ValueError("MAIN_DIRECTORY not set in environment variables") 

    # Create log folder 
    log_folder = Path(default_directory) / "logs" 
    log_folder.mkdir(parents=True, exist_ok=True) 

    # Set logger level 
    logger.setLevel(logging.DEBUG)

    # File handler with rotation (10MB, 5 backups) 
    file_handler = RotatingFileHandler( 
        filename = log_folder / f"application_{today}.log", 
        maxBytes=10 * 1024 * 1024,  # 10MB 
        backupCount=5, 
        encoding='utf-8' 
    ) 

    file_handler.setLevel(logging.DEBUG)

    # Console handler (only warnings and above) 
    console_handler = logging.StreamHandler() 
    console_handler.setLevel(logging.WARNING) 

    # Detailed formatter with function name and line number 
    formatter = logging.Formatter( 
        '%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S' 
    ) 

    # Apply formatter to handlers 
    file_handler.setFormatter(formatter) 
    console_handler.setFormatter(formatter) 

    # Add handlers to logger 
    logger.addHandler(file_handler) 
    logger.addHandler(console_handler) 

    return logger 