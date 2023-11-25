import csv
from abc import ABC, abstractmethod
from typing import Any
from collections import defaultdict
import os
from torch.utils.tensorboard import SummaryWriter
import datetime
import logging
import colorful as cf
import torch.distributed as dist
from itertools import zip_longest
__all__ = ["coflogger","cofcsv","coftb"]
allocated_loggers = {}

def is_rank0():
    if (not dist.is_initialized()) or dist.get_rank()==0:
        return True
    else:
        return False

class Logger(logging.Logger):
    DEBUG=logging.DEBUG
    INFO=logging.INFO
    WARN=logging.WARN
    WARNING=logging.WARNING
    FATAL=logging.FATAL
    CRITICAL=logging.CRITICAL
    PRANK = 999
    
    def default_color(self, x): return x
    color_to_rank = [
        cf.italic_red,
        cf.italic_yellow,
        cf.italic_cyan,
        cf.italic_orange,
        cf.italic_blue,
        cf.italic_magenta,
        cf.italic_green,
        cf.italic_purple,
    ]
    def __init__(self, name):
        super(Logger, self).__init__(name)
        self.tag = "Cof"
        self.print_thread = False
        self.print_level = True
        self.rank = 0
        self.name2handler = dict()
        logging.Logger.setLevel(self, logging.DEBUG)

        
    def add_log_file(self, log_file:str, name:str=""):
        if not name: name = log_file
        if name in self.name2handler: return
        handler = logging.FileHandler(log_file)
        self.name2handler[name] = handler
        self.addHandler(handler)
        self.reset_format()

    def set_level_for_handler(self, name:str, level:int):
        if name not in self.name2handler: return
        handler: logging.Handler = self.name2handler[name]
        handler.setLevel(level)
        
    def set_level_for_all(self, level:int):
        for name in self.name2handler:
            handler: logging.Handler = self.name2handler[name]
            handler.setLevel(level)
    
    def setLevel(self, *args, **kwargs):
        print(f"Warn: `setLevel` is not supported, use `set_level_for_all` instead")
        
        
        
    def generate_fmt(self)->logging.StreamHandler:
        level_fmt = "" if not self.print_level else f" [{self.tag} %(levelname)s]"
        basic_fmt = f'[%(asctime)s.%(msecs)03d] {level_fmt}: %(message)s'
        date_fmt = "%Y-%m-%d %H:%M:%S"
        fmt = logging.Formatter(
            fmt = basic_fmt,
            datefmt = date_fmt
        )
        return fmt
        
    def reset_format(self):
        formatter = self.generate_fmt()
        for handler in self.handlers: 
            handler.setFormatter(formatter)
        return self
            
    def _set_tag(self, tag:str):
        self.tag = tag
        self.reset_format()
        return self
    def debug(self, msg:str, color:str='',*args, **kwargs):
        '''print with rank. If color is not specified, use the color format corresponding to the rank'''
        if is_rank0():
            if not self.isEnabledFor(self.DEBUG): return
            color = getattr(cf, color) if color else self.default_color
            self._log(self.DEBUG, color(msg), args, **kwargs)
    def info(self, msg:str, *args, **kwargs):
        if is_rank0():
            if self.isEnabledFor(logging.INFO): self._log(logging.INFO, cf.green(msg), args, kwargs)
    def warn(self, msg:str, *args, **kwargs):
        if is_rank0():
            if self.isEnabledFor(logging.WARN): self._log(logging.WARN, cf.yellow(msg), args, kwargs)
    def error(self, msg:str, *args, **kwargs):
        if is_rank0():
            if self.isEnabledFor(logging.ERROR): self._log(logging.ERROR, cf.red(msg), args, kwargs)
        
    warning = warn
 
def get_level_from_env(logger_name:str, default_level="info"):
    level = default_level if logger_name not in os.environ else os.environ[logger_name]
    level = level.lower()
    level2num = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARN,
        "warning": logging.WARN,
        "error": logging.ERROR
    }
    if level in level2num: return level2num[level]
    print(f"Unknown level {level} for logger {logger_name}, use default level {default_level}")
    return level2num[default_level]  

def get_logger(logger_name="COF_DEBUG",
               enable_console = True)->Logger:
    if logger_name in allocated_loggers: return allocated_loggers[logger_name]
    # why need to call `setLoggerClass` twice? refer to the issue: https://bugs.python.org/issue37258
    logging.setLoggerClass(Logger)
    logger:Logger = logging.getLogger(logger_name)
    logging.setLoggerClass(logging.Logger)
    # Initilize level from environment. If not specified, use INFO
    if enable_console:
        streamHandler = logging.StreamHandler()
        name = logger_name
        logger.name2handler[name] = streamHandler
        streamHandler.setLevel(get_level_from_env(logger_name))
        logger.addHandler(streamHandler)
    logger.reset_format()
    allocated_loggers[logger_name] = logger
    return logger

class BaseWriter(ABC):
    def __init__(self, file_path) -> None:
        self.file_path = file_path

    @abstractmethod
    def write(self, data):
        pass

class Coftb(BaseWriter):
    def __init__(self, file_path='coftb') -> None:
        super().__init__(file_path)
        self.writer=None
    def __call__(self, name=None):
        if (not is_rank0()) or self.writer is not None:
            return
        if name:
            formatted_name = name
        else:
            now = datetime.datetime.now()
            formatted_name = now.strftime("%m%d%H%M%S")

        self.writer = SummaryWriter(os.path.join(self.file_path, formatted_name))
        self.iter_dict = defaultdict(int)
    def write(self, data:dict):
        if self.writer is None:
            return
        for k,v in data.items():
            self.iter_dict[k]+=1
            self.writer.add_scalar(k, v, self.iter_dict[k])
    def close(self):
        if self.writer is None:
            return
        self.writer.close()

class _Cofcsv(BaseWriter):
    def __init__(self, file_path=None) -> None:
        super().__init__(file_path)
        self.table=defaultdict(list)

    def write(self, data_dict:dict):
        for k, v in data_dict.items():
            self.table[k].append(v)
        
    def save(self, file_prefix, reset):
        data=[]
        if not self.table:
            return
        data.append(self.table.keys())
        for each in zip_longest(*self.table.values()):
            data.append(list(each))
        with open(f'{file_prefix}.csv', 'w', newline='') as fp:
            writer = csv.writer(fp)
            for data_row in data:
                writer.writerow(data_row)
        if reset:
            self.table.clear()

class Cofcsv:
    def __init__(self) -> None:
        self.table=defaultdict(_Cofcsv)

    def __call__(self, name) -> _Cofcsv:
        return self.table[name]
    
    def save(self, root_dir='.', reset=True) -> None:
        if not is_rank0():
            return
        if not (os.path.exists(root_dir) and os.path.isdir(root_dir)):
            os.mkdir(root_dir)
        for key, value in self.table.items():
            value.save(os.path.join(root_dir,key), reset)
        
coflogger = get_logger()
cofcsv = Cofcsv()
coftb = Coftb()

WRITER_TABLE={
    "tb": coftb.write,
    "csv": None,
    "debug":coflogger.debug,
    "info": coflogger.info,
    "warn": coflogger.warn,
    "error": coflogger.error,
}