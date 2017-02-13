#encoding:utf-8

import os
import logging
from logging import StreamHandler, FileHandler
from setting import LOG_DEFAULT_FILE

RESET_COLOR = '\033[0m'
stream_fmt = '%(name)s [%(color)s%(levelname)s' + RESET_COLOR + ']: %(message)s' 

class ColorStreamHandler(logging.StreamHandler):
    """
    Color of stream log format.
    """
    LEVEL_COLORS = {
        logging.DEBUG: '',  # SYSTEM
        logging.INFO: '\033[00;36m',  # CYAN
        logging.WARN: '\033[01;33m',  # BOLD YELLOW
        logging.ERROR: '\033[01;31m',  # BOLD RED
        logging.CRITICAL: '\033[01;31m',  # BOLD RED
    }

    def format(self, record):
        record.__dict__['color'] = self.LEVEL_COLORS[record.levelno]
        return logging.StreamHandler.format(self, record)


class Logger(object):
    def __init__(self, name, log_file, log_level='INFO'):
        """
        :param log_file: the path of log file
        :param log_level: the log level which can be "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        """
        # create logger
        self.logger = logging.getLogger(name)
        log_level = self._convert_log_level(log_level)
        self.logger.setLevel(log_level)
        
        # Remove the existed handlers belonging to the logger
        handlers = self.logger.handlers
        while len(handlers) != 0:
            self.logger.removeHandler(handlers[0])
                
        # create console and file handler and set log level  
        self.ch = None
        self.fh = None
        ch = ColorStreamHandler()
        ch.setLevel(log_level)
        fh = FileHandler(log_file)
        fh.setLevel(log_level)     
        
        # create formatter
        #formatter = logging.Formatter('%(asctime)s - %(filename)s - %(lineno)s - %(levelname)s - %(message)s')
        global stream_fmt
        ch_formatter = logging.Formatter(stream_fmt)
        fh_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # add formatter to handlers
        ch.setFormatter(ch_formatter)
        fh.setFormatter(fh_formatter)
        
        # add handlers to logger
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)
       
        self.ch = ch
        self.fh = fh
        
    def _convert_log_level(self, log_level):
        log_convert_dict = {'DEBUG': logging.DEBUG,
                            'INFO': logging.INFO,
                            'WARNING': logging.WARNING,
                            'ERROR': logging.ERROR,
                            'CRITICAL': logging.CRITICAL}
        return log_convert_dict[log_level]

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def exit(self):
        if self.ch is not None:
            self.logger.removeHandler(self.ch)
        if self.fh is not None:
            self.logger.removeHandler(self.fh)

def get_logger(name, log_file=None, log_level='INFO'):
    if log_file is None:
        log_file = LOG_DEFAULT_FILE
    if os.path.isfile(log_file):
        pass
    else:
        log_dir = os.path.dirname(log_file)
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir) 
        with open(log_file, 'w'):
            pass
    logger = Logger(name, log_file, log_level=log_level)
    return logger

if __name__ == '__main__':
    w = get_logger('TEST')
    w.info('wwwwwwwww')
