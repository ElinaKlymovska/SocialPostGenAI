import logging

# Define the configuration for logging
LOG_FILE = "application.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.DEBUG

# Configure logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Utility function to get a logger
def get_logger(name):
    """Returns a logger instance with the specified name."""
    return logging.getLogger(name)
