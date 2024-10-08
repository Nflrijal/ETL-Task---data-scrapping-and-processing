import logging

def setup_logger(name):
    # Create a logger
    logger = logging.getLogger(name)

    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to the handler
    console_handler.setFormatter(formatter)

    # Add the handler to the logger if it hasn't been added already
    if not logger.hasHandlers():
        logger.addHandler(console_handler)

    return logger
