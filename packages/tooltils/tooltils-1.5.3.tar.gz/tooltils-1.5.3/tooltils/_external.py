"""External backend file meant to handle functions that would cause import errors"""


from importlib import import_module
from logging import getLogger
from ast import literal_eval


module = None

class levelFilter(object):
    def __init__(self, level):
        self.level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.level

def create(module: str, level: str, level2: str):
    logger = getLogger(module)

    logger.setLevel(level)
    logger.addFilter(levelFilter(level2))

    return logger

def enable(logger, enabled: bool, closed: bool) -> None:
    if closed: raise ValueError('The logger has already been closed')

    if enabled:
        raise ValueError('The logger is already enabled')
    else:
        logger.disabled = False

def disable(logger, enabled: bool, closed: bool) -> None:
    if closed: raise ValueError('The logger has already been closed')

    if not enabled:
        raise ValueError('The logger is already disabled')
    else:
        logger.disabled = True

def close(logger, closed: bool) -> None:
    if closed:
        raise ValueError('The logger has already been closed')
    else:
        logger.disabled = True
        logger.close()

def run(funcName: str, args: str):
    global module

    try:
        args = list(literal_eval(args))

        if funcName.startswith('tooltils'):
            if module is None:
                module = import_module('tooltils')
            
            if len(funcName.split('.')) == 2:
                return getattr(module, funcName.split('.')[1])(*args)
            else:
                return getattr(getattr(module, funcName.split('.')[1]), funcName.split('.')[2])(*args)
        else:
            for k, v in globals()['__builtins__'].items():
                if k == funcName:
                    return v(*args)
    except:
        return None
