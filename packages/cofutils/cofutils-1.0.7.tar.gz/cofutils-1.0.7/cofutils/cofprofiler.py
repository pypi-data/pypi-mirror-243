import time
import torch
from .cofwriter import coflogger, coftb, WRITER_TABLE,cofcsv
from typing import Any

def parse_writer(writer:str):
    if writer is None:
        return None
    assert isinstance(writer,str), "writer type error; writer must be a string"
    writers = [item.strip() for item in writer.split(',') if item.strip() in WRITER_TABLE.keys()]
    if len(writers) == 0:
        writers = None
    return writers

class BaseProfiler:
    def __init__(self) -> None:
        self.writers=None
    def set_writer(self, writer:str=None, name='cofdefault'):
        self.writers = parse_writer(writer=writer)
        if self.writers is None:
            return
        if 'tb' in self.writers:
            coftb(name)
        if 'csv' in self.writers:
            WRITER_TABLE['csv'] = cofcsv(name).write

class _Timer:
    """Timer."""

    def __init__(self, name, cuda_timer=False):
        self.name_ = name
        self.elapsed_ = 0.0
        self.started_ = False
        self.cuda_timer = cuda_timer
        self.event_timers = []

    def __enter__(self):
        self.start()
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def start(self):
        """Start the timer."""
        assert not self.started_, 'timer has already been started'
        if not self.cuda_timer:
            self.start_time = time.time()
        else:
            self.start_event = torch.cuda.Event(enable_timing=True)
            self.start_event.record()

        self.started_ = True

    def stop(self):
        """Stop the timer."""
        assert self.started_, 'timer is not started'
        # self.elapsed_ += (time.time() - self.start_time)
        if not self.cuda_timer:
            self.event_timers.append(time.time() - self.start_time)
        else:
            end_event = torch.cuda.Event(enable_timing=True)
            end_event.record()
            self.event_timers.append((self.start_event, end_event))
            self.start_event = None
        self.started_ = False

    def reset(self):
        """Reset timer."""
        self.elapsed_ = 0.0
        self.started_ = False
        self.start_event = None
        self.event_timers.clear()

    def elapsed(self, reset=True):
        """Calculate the elapsed time."""
        started_ = self.started_
        # If the timing in progress, end it first.
        if self.started_:
            self.stop()
        # Get the elapsed time.
        def cuda_event_time(start,end):
            torch.cuda.current_stream().wait_event(end)
            end.synchronize()
            return start.elapsed_time(end)
        if not self.cuda_timer:
            elapsed_ = sum([each*1000 for each in self.event_timers])
        else:
            # cuda event elapsed time return in ms
            elapsed_ = sum([cuda_event_time(each[0],each[1]) for each in self.event_timers])

        # Reset the elapsed time
        if reset:
            self.reset()
        # If timing was in progress, set it back.
        if started_:
            self.start()
        return elapsed_
    
class Coftimer(BaseProfiler):
    """Group of timers."""

    def __init__(self):
        super(Coftimer, self).__init__()
        self.timers = {}

    def __call__(self, name, cuda_timer=False):
        if name not in self.timers:
            self.timers[name] = _Timer(name, cuda_timer)
        return self.timers[name]
    
    def log(self, normalizer=1.0, timedict=False):
        """Log a group of timers."""
        assert normalizer > 0.0

        string = 'time (ms)'
        reset=True
        names = self.timers.keys()
        time_dict = {
                name:self.timers[name].elapsed(
                    reset=reset) / normalizer for name in names
            }
        if timedict:
            return time_dict
        for k,v in time_dict.items():
            string += ' | {}: {:.2f}'.format(k, v)

        if self.writers is None:
            coflogger.info(string)
            return
        
        for writer in self.writers:
            if writer in ['tb', 'csv']:
                # write time profiling results in dictionary format
                WRITER_TABLE[writer](time_dict)
            elif writer in ['debug','info','warn','error']:
                # cof logger print out time result in string format
                WRITER_TABLE[writer](string)
            else:
                # use coflogger.info in default
                coflogger.info(string)
        return None

class Cofmem(BaseProfiler):
    def __init__(self) -> None:
        super(Cofmem, self).__init__()
        
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.report_memory_usage(*args, **kwds)

    def report_memory_usage(self, msg=""):
        # MC: Memory Allocated in Current
        # MM: Memory Allocated in Max
        # MR: Memory Reserved by PyTorch
        if self.writers is None:
            # memory report API is time-cost; therefore, do nothing if user don't specify the writer
            return
        GB = 1024*1024*1024
        MA = torch.cuda.memory_allocated()/GB
        MM = torch.cuda.max_memory_allocated()/GB
        MR = torch.cuda.memory_reserved()/GB
        memory_report_string = f"{msg} GPU Memory Report (GB): MA = {MA:.2f} | "\
                        f"MM = {MM:.2f} | "\
                        f"MR = {MR:.2f}"
        memory_report_dict = {'MA':MA, 'MM':MM, 'MR':MR}

        for writer in self.writers:
            if writer in ['tb', 'csv']:
                # write time profiling results in dictionary format
                WRITER_TABLE[writer](memory_report_dict)
            elif writer in ['debug','info','warn','error']:
                # cof logger print out time result in string format
                WRITER_TABLE[writer](memory_report_string)
            else:
                # default
                coflogger.info(memory_report_string)



import ctypes

_cudart = ctypes.CDLL('libcudart.so')

class Cofnsys:
    def __init__(self) -> None:
        pass
    @staticmethod
    def start():
        # As shown at http://docs.nvidia.com/cuda/cuda-runtime-api/group__CUDART__PROFILER.html,
        # the return value will unconditionally be 0. This check is just in case it changes in 
        # the future.
        ret = _cudart.cudaProfilerStart()
        if ret != 0:
            raise Exception("cudaProfilerStart() returned %d" % ret)
    @staticmethod
    def stop():
        ret = _cudart.cudaProfilerStop()
        if ret != 0:
            raise Exception("cudaProfilerStop() returned %d" % ret)
    @staticmethod
    def nvtx(func):
        """decorator that causes an NVTX range to be recorded for the duration of the
        function call."""
        def wrapped_fn(*args, **kwargs):
            torch.cuda.nvtx.range_push(func.__qualname__)
            ret_val = func(*args, **kwargs)
            torch.cuda.nvtx.range_pop()
            return ret_val
        return wrapped_fn

cofnsys = Cofnsys()
cofmem = Cofmem()
coftimer=Coftimer()
