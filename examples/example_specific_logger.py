import logging

import reger

logger = logging.getLogger('TestLogger')
reger.setup_logging(logger=logger)

logger.info('Hello, reger!')
logger.debug('This is debug')
logger.warning('This is warning')
logger.error('This is error')
logger.critical('This is critical!!')
