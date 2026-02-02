import inspect as _inspect
import sys as _sys, os as _os, time as _time
import subprocess as _subprocess, shlex as _shlex
import math


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # #                                                                                   # # # # #
# # # # #                                   DEBUGGING                                       # # # # #
# # # # #                                                                                   # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 1.1 Get current Line Number with __line__() or __line__
# usage: print(f"This is line no {__line__} in the file")

"""
# usage: print(f"This is line no {__line__()}")
def __line__():
    # return _inspect.currentframe().f_back.f_lineno
    return _sys._getframe(1).f_lineno
"""
class _Line:
    def __str__(self):
        # return str(_inspect.currentframe().f_back.f_lineno)
        return str(_sys._getframe(1).f_lineno)
    def __int__(self):
        return int(str(self))
__line__ = _Line()

# 1.2 Simple Timer Context Manager
# Usage: with timer(): do_heavy_stuff()
class timer:
    def __enter__(self):
        self.start = _time.time()
        return self
    def __exit__(self, *args):
        print(f"Executed in: {_time.time() - self.start:.8f}s")

# 1.3 "What is this?" Inspector
# Prints the variable name AND value. Great for quick debugging.
# Usage: dump(my_complex_list) -> "my_complex_list: [...]"
def dump(var):
    # This magic looks at the code that called this function to find the variable name
    frame = _inspect.currentframe().f_back
    try:
        call_line = _inspect.getframeinfo(frame).code_context[0]
        var_name = call_line.strip().split('(')[1][:-1]
        print(f"{var_name}: {var}")
    except:
        print(f"?: {var}")

# 1.4 Print variable with name and value
# Print variable names and values
def dbg(*vars):
    frame = _inspect.currentframe().f_back
    for var in vars:
        var_name = None
        for name, value in frame.f_locals.items():
            if value is var:
                var_name = name
                break
        print(f"{var_name if var_name else 'Unknown'} = {var}")
    return vars[0] if len(vars) == 1 else vars

# 1.5 Print variables with line numbers and values
def spy(*args):
    current_file = _os.path.normcase(__file__)
    frame = _sys._getframe(1)

    while frame:
        frame_file = _os.path.normcase(frame.f_code.co_filename)
        if frame_file != current_file:
            break
        frame = frame.f_back

    if not frame:
        frame = _sys._getframe(1)

    print(f"[Line {frame.f_lineno}]", *args)





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # #                                                                                   # # # # #
# # # # #                                   LISTS & STRING                                  # # # # #
# # # # #                                                                                   # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# 2.1 Remove falsy and truthy values from the list and return the new list
rm_falsy = lambda unfiltered_list: list(filter(bool, unfiltered_list))
rm_truthy = lambda unfiltered_list: [i for i in unfiltered_list if not i]

# 2.2 Flatten a list
"""
def flatten_l(nested_list):
    if not(bool(nested_list)):
        return nested_list

    if isinstance(nested_list[0], list):
        return flatten_l(*nested_list[:1]) + flatten_l(nested_list[1:])

    return nested_list[:1] + flatten_list(nested_list[1:])
"""

def flatten_l(obj):
    if isinstance(obj, (list, tuple)): # if we want to support both list and tuples
    # if isinstance(obj, list):
        for item in obj:
            yield from flatten_l(item)
    else:
        yield obj

# Only for list of lists (depth is only 2)
# flatten_l = lambda nested_list: list(_itertools.chain.from_iterable(nested_list))

# 2.3 Chunk a list into smaller lists of size n
# Usage: batched_l([1,2,3,4,5], 2) -> [[1,2], [3,4], [5]]
batched_l = lambda l, n: [l[i:i + n] for i in range(0, len(l), n)]

# 2.4 Unique list (Preserving Order)
# set(l) destroys order. This keeps it.
# Usage: uniq_l([3, 1, 2, 1, 3]) -> [3, 1, 2]
uniq_l = lambda l: list(dict.fromkeys(l))

# 2.5 Transpose a matrix (list of lists)
# Turns rows into columns. Very useful for grid-based algo problems.
# Usage: trans_l([[1,2], [3,4]]) -> [(1,3), (2,4)]
trans_l = lambda l: list(map(list, zip(*l)))


# 2.6 Find first matching element
# Return first element satisfying condition or None
def find_first(l, condition):
    return next((x for x in l if condition(x)), None)

# 2.7 Find first matching index
def find_first_ind(l, condition):
    return next((i for i in range(len(l)) if condition(l[i])), None)

# 2.8 Find all indices of element
# Return all indices where condition is True
def find_inds(l, condition):
    return [i for i, x in enumerate(l) if condition(x)]

# 2.9 Split list by condition
# Split list into (matching, non_matching)
def split_by(l, condition):
    matching = []
    non_matching = []
    for x in l:
        (matching if condition(x) else non_matching).append(x)
    return matching, non_matching

# 2.10 Remove empty strings from list
rm_empty_str = lambda l: [s for s in l if s.strip()]

# 2.11 Join list with custom separator
join_with = lambda l, sep: sep.join(map(str, l))

# 2.12 Split string and strip whitespace
# Split string and strip each element
def split_strip(s, delimiter=None):
    return [part.strip() for part in s.split(delimiter)]

# 2.13 Reverse a list and return the reversed list
rev_l = lambda l: list(reversed(l))





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # #                                                                                   # # # # #
# # # # #                                   DICTS                                           # # # # #
# # # # #                                                                                   # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 3.1 Sort a dictionary
def sort_d(d, k_or_v='k'):
    if k_or_v == 'k': return {k: v for k, v in sorted(d.items(), key=lambda item: item[0])}
    elif k_or_v == 'v': return {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}

sort_d_k = lambda d: {k:v for k,v in sorted(d.items(), key=lambda item: item[0])}
sort_d_v = lambda d: {k:v for k,v in sorted(d.items(), key=lambda item: item[1])}
sort_d_kv = lambda d: {k:v for k,v in sorted(d.items(), key=lambda item: (item[0], item[1]))}
sort_d_vk = lambda d: {k:v for k,v in sorted(d.items(), key=lambda item: (item[1], item[0]))}

# 3.2 Filter dictionary by keys
filter_d_k = lambda d, fn: {k:v for k,v in d.items() if fn(k)}

# 3.3 Filter dictionary by values
filter_d_v = lambda d, fn: {k:v for k,v in d.items() if fn(v)}

# 3.4 Get value or default (but shorter and explicit)
get_d = lambda d, k, default=None: d[k] if k in d else default

# 3.5 Get multiple keys safely
get_ds = lambda d, ks, default=None: [d[k] if k in d else default for k in ks]

# 3.6 Reverse a dictionary (key, value) to (value, key)
rev_d = lambda d: {v:k for k,v in d.items()}
rev_d_vk = lambda d: {v:k for k,v in d.items()}


# 3.7 itertools.groupby() but values are list
def groupby_l(l, key_fn):
    d = {}
    for item in l:
        k = key_fn(item)
        d.setdefault(k, []).append(item)
    return d

# 3.8 collections.Counter() but quick
def counter_l(l):
    d = {}
    for i in l:
        d[i] = d.get(i, 0) + 1
    return d




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # #                                                                                   # # # # #
# # # # #                                     FILE HANDLING                                 # # # # #
# # # # #                                                                                   # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 4.1 Read file content as string
read_f = lambda filename: open(filename, 'r', encoding='utf-8').read()

# 4.2 Write string to file
write_f = lambda filename, content: open(filename, 'w', encoding='utf-8').write(content)

# 4.3 Read file as lines (stripping newline chars)
read_lines_f = lambda filename: [line.strip() for line in open(filename, 'r', encoding='utf-8')]

# 4.4 Write lines to file
# Write list of strings to file
def write_lines_f(filepath, lines):
    with open(filepath, 'w') as f: f.write('\n'.join(lines))

# 4.5 Count lines in file efficiently
# Count lines in file without reading entire file
def count_lines_f(filepath):
    with open(filepath, 'rb') as f: return sum(1 for _ in f)





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # #                                                                                   # # # # #
# # # # #                                     SHELL                                         # # # # #
# # # # #                                                                                   # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# 7.1 Run a shell command and store the value as we see in the terminal
def shell(command):
    # shlex.split handles quotes correctly: 'echo "hello world"' -> ['echo', 'hello world']
    parts = _shlex.split(command)
    return _subprocess.run(parts, stdout=_subprocess.PIPE).stdout.decode('utf-8').splitlines()

# 7.2 Run shell command with error handling
def sh(command):
    """Run command, return (success, output)"""
    try:
        result = _subprocess.run(command, shell=True, capture_output=True, text=True)
        return (result.returncode == 0, result.stdout.strip())
    except Exception as e: return (False, str(e))





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # #                                                                                   # # # # #
# # # # #                                     MATH                                          # # # # #
# # # # #                                                                                   # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def int_to_base(n, base):
    if n == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" # len(digits) = 36
    if not (2 <= base <= 36):
        raise ValueError("Base must be between 2 and 36")
    sign = "-" if n < 0 else ""
    n = abs(n)
    result = ""
    while n > 0:
        result = digits[n % base] + result
        n //= base
    return sign + result


def from_to_base(num_str, from_base, to_base):
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" # len(digits) = 36

    # For base 62 support digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    if not (2 <= from_base <= 36) or not (2 <= to_base <= len(digits)):
        raise ValueError(f"Bases must be between 2 and {len(digits)}")

    try:
        decimal_value = int(num_str, from_base)
    except ValueError:
        raise ValueError(f"'{num_str}' is not a valid base-{from_base} number.")


    is_negative = decimal_value < 0
    abs_value = abs(decimal_value)
    if abs_value == 0:
        return "0"

    res = ""
    while abs_value > 0:
        abs_value, remainder = divmod(abs_value, to_base)
        res = digits[remainder] + res

    return "-" + res if is_negative else res





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # #                                                                                   # # # # #
# # # # #                                     MISC                                          # # # # #
# # # # #                                                                                   # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Calculate percentage safely
def percentage(part, whole):
    return (part / whole * 100) if whole else 0

# Pipe functions (like Unix pipe)
# Chain functions: pipe(f, g, h)(x) = h(g(f(x)))
# Chain functions (using reversed funcs): pipe(h, g, f)(x) = h(g(f(x)))
def pipe(*funcs):
    def _pipe(initial):
        result = initial
        for func in reversed(funcs):
            result = func(result)
        return result
    return _pipe


def minmax(values):
    minimum, maximum = math.inf, -math.inf
    for v in values:
        if v < minimum:
            minimum = v
        if v > maximum:
            maximum = v
    return minimum, maximum
