from config.settings import Settings
import logging

def setup_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)

    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }

    level_name = Settings.LOG_LEVEL.upper()
    level = log_levels.get(level_name)

    if level is None:
        logger.warning(f"Invalid log level: {Settings.LOG_LEVEL}. Using default (INFO).")
        level = logging.INFO 

    logging.basicConfig(
        format=(
            '%(asctime)s '
            '%(levelname)s '
            '%(funcName)s#%(lineno)d: '
            '%(message)s'
        ),
        datefmt='%Y-%m-%dT%H:%M:%S%z'
    )

    logger.setLevel(level)

    return logger