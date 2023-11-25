# import logging
import logging

from colorlog import ColoredFormatter

# Define the new logging level value and name
TASK_LEVEL = 25
logging.addLevelName(TASK_LEVEL, "TASK")

logger = logging.getLogger("airflow.task")


stream = logging.StreamHandler()
log_format = "%(reset)s%(log_color)s%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s \n"
stream.setFormatter(
    ColoredFormatter(
        log_format,
        log_colors={
            "TASK": "bold_green",
            "INFO": "cyan",
            "ADDITIONAL INFO": "green",
            "DEBUG": "yellow",
            "WARNING": "red",
            "ERROR": "red",
            "CRITICAL": "black,bg_red",
        },
    )
)

# Register the new logging level
logging.addLevelName(TASK_LEVEL, "TASK")
logging.Logger.task = lambda self, msg, *args, **kwargs: self.log(TASK_LEVEL, msg, *args, **kwargs)

logger.addHandler(stream)
logger.setLevel(logging.DEBUG)
