import logging

import reger

root_logger = logging.getLogger()

file_handler = logging.FileHandler('./latest.log')
file_handler.setFormatter(reger.ColourFormatter())
root_logger.addHandler(file_handler)

reger.setup_logging(logger=root_logger)

logging.info('Hello, reger!')
logging.debug('This is debug')
logging.warning('This is warning')
logging.error('This is error')
logging.critical('This is critical!!')
