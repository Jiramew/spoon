import logging
import os
from logging.handlers import TimedRotatingFileHandler

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)

log_fmt = '%(asctime)s\tFile \"%(filename)s\",line %(lineno)s\t%(levelname)s: %(message)s'
formatter = logging.Formatter(log_fmt)
log_file_handler = TimedRotatingFileHandler(filename=os.path.join(log_path, "spoon.log"), when="D", interval=1)
log_file_handler.suffix = '%Y%m%d.log'
log_file_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
log.addHandler(log_file_handler)
