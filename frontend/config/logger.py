"""
Натройка логгирования    
"""
import logging


file_log = logging.FileHandler('frontend.log', 'a+')
console_out = logging.StreamHandler()
logging.basicConfig(
    handlers=(file_log, console_out),
    level=logging.INFO,
    format=u'[%(asctime)s] %(filename)s:%(lineno)d #%(levelname)-4s %(name)s: %(message)s',
)

logger = logging.getLogger("frontend")
