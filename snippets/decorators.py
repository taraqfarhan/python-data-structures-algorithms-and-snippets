from time import perf_counter
from functools import wraps

DEFAULT_FMT = "[{elapsed:.8f}s] {name}({args}) -> {result}"
# benchmark (ben)
def ben(fmt=DEFAULT_FMT):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = perf_counter()
            result = func(*args, **kwargs)
            elapsed = perf_counter() - start

            name = func.__name__
            args = [repr(arg) for arg in args]
            args.extend({f"{k}={v}" for k,v in kwargs.items()})
            args = ', '.join(args)
            print(fmt.format(**locals()))

            return result
        return wrapper
    return decorator

