import cProfile
import pstats
import io
import time
from functools import wraps

def profile_performance(func):
    """
    A decorator that utilizes cProfile to trace absolute execution bottlenecks
    down to the microsecond. Extremely useful for identifying array duplication
    during OpenCV operations.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        pr.disable()
        
        s = io.StringIO()
        sortby = pstats.SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats(15) # Print top 15 most expensive calls
        
        print(f"\n--- Performance Profiler: {func.__name__} ---")
        print(f"Total Execution Time: {(end_time - start_time):.4f} seconds")
        print(s.getvalue())
        
        return result
    return wrapper

class AsyncProfiler:
    """
    A context manager approach for profiling Async methods,
    since cProfile decorators act weirdly on asyncio Coroutines.
    """
    def __init__(self, name="AsyncBlock"):
        self.name = name
        self.pr = cProfile.Profile()
        
    def __enter__(self):
        self.start_time = time.time()
        self.pr.enable()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pr.disable()
        end_time = time.time()
        
        s = io.StringIO()
        ps = pstats.Stats(self.pr, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
        ps.print_stats(15)
        
        print(f"\n--- Async Performance Profiler: {self.name} ---")
        print(f"Total Execution Time: {(end_time - self.start_time):.4f} seconds")
        print(s.getvalue())
