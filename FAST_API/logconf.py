from pydantic_settings import BaseSettings

logs_target = r"C:\Users\KT\inzynierka\FAST_API\logs\medical_images_server.log"

class LogConfig(BaseSettings):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "main_logger"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        'standard': { 
            "class": "logging.Formatter",
            "format": "%(asctime)s\t%(levelname)s\t%(filename)s\t%(message)s",
            "datefmt": "%d %b %y %H:%M:%S"
        },
    }
    handlers: dict = {
        # "default": {
        #     "formatter": "default",
        #     "class": "logging.StreamHandler",
        #     "stream": "ext://sys.stderr",
        # },
        "file": {  
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "filename": logs_target,
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 500000
        }
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["file"], "level": LOG_LEVEL},
    }