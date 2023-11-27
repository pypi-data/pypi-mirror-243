import datetime
import inspect
import os.path
import sys
from fishhook import hook
from functools import wraps
from typing import Any


class Cache(dict):
    def __init__(self):
        super().__init__()
        self.hits = 0
        self.misses = 0

    def str_hits(self) -> str:
        return "%d (%1.2f)" % (self.hits, self.hits / (self.misses + self.hits) * 100)

    def __contains__(self, item: Any) -> bool:
        r = super().__contains__(item)
        if r:
            self.hits += 1
        else:
            self.misses += 1

        return r


class Dict(dict):
    _initialized: bool = False

    def __init__(self, *args, **kwargs):
        if "default" in kwargs:
            self.__default = kwargs["default"]
            del kwargs["default"]
        else:
            self.__default = None

        super(Dict, self).__init__(*args, **kwargs)
        self.convert()
        self._initialized = True

    def convert(self):
        for k in self:
            if isinstance(self[k], dict) and not isinstance(self[k], Dict):
                self[k] = Dict(self[k])
            elif isinstance(self[k], list):
                for i in range(len(self[k])):
                    if isinstance(self[k][i], dict) and not isinstance(
                        self[k][i], Dict
                    ):
                        self[k][i] = Dict(self[k][i])

    def update(self, other: dict, **kwargs):
        super(Dict, self).update(other, **kwargs)
        self.convert()

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            if self.__default is None:
                raise AttributeError(item)
            else:
                return self.__default

    def __setattr__(self, key, value):
        if not self._initialized:
            super(Dict, self).__setattr__(key, value)
        else:
            self[key] = value

    def __setitem__(self, key, value):
        super(Dict, self).__setitem__(key, value)
        self.convert()


def get_script_dir(follow_symlinks: bool = True) -> str:
    """return path of the executed script"""
    if getattr(sys, "frozen", False):
        path = os.path.abspath(sys.executable)
    else:
        if "__main__" in sys.modules and hasattr(sys.modules["__main__"], "__file__"):
            path = sys.modules["__main__"].__file__
        else:
            path = inspect.getabsfile(get_script_dir)

    if follow_symlinks:
        path = os.path.realpath(path)

    return os.path.dirname(path)


def compare(a: Any, b: Any) -> int:
    """compare to values, return -1 if a is smaller than b, 1 if a is greater than b, 0 is both are equal"""
    return bool(a > b) - bool(a < b)


def minmax(*arr: Any) -> (Any, Any):
    """return the min and max value of an array (or arbitrary amount of arguments)"""
    if len(arr) == 1:
        if isinstance(arr[0], list):
            arr = arr[0]
        else:
            return arr[0], arr[0]

    arr = set(arr)
    smallest = min(arr)
    biggest = max(arr)
    if smallest == biggest:
        arr.remove(smallest)
        biggest = max(arr)

    return smallest, biggest


def human_readable_time_from_delta(delta: datetime.timedelta) -> str:
    time_str = ""
    if delta.days > 0:
        time_str += "%d day%s, " % (delta.days, "s" if delta.days > 1 else "")

    if delta.seconds > 3600:
        time_str += "%02d:" % (delta.seconds // 3600)
    else:
        time_str += "00:"

    if delta.seconds % 3600 > 60:
        time_str += "%02d:" % (delta.seconds % 3600 // 60)
    else:
        time_str += "00:"

    return time_str + "%02d" % (delta.seconds % 60)


def human_readable_time_from_ns(ns: int) -> str:
    units = [
        (1000, "ns"),
        (1000, "µs"),
        (1000, "ms"),
        (60, "s"),
        (60, "m"),
        (60, "h"),
        (24, "d"),
    ]

    time_parts = []
    for div, unit in units:
        ns, p = ns // div, ns % div
        time_parts.insert(0, "%d%s" % (p, unit))
        if ns == 0:
            return ", ".join(time_parts)


def cache(func):
    saved = {}

    @wraps(func)
    def new_func(*args):
        if args in saved:
            return saved[args]

        result = func(*args)
        saved[args] = result
        return result

    return new_func


@hook(list)
def intersection(self, *args) -> list:
    ret = set(self).intersection(*args)
    return list(ret)


@hook(list)
def __and__(self, *args) -> list:
    return self.intersection(*args)


@hook(str)
def intersection(self, *args) -> str:
    ret = set(self).intersection(*args)
    return "".join(list(ret))


@hook(str)
def __and__(self, *args) -> str:
    return self.intersection(*args)


@hook(int)
def sum_digits(self) -> int:
    s = 0
    num = self
    while num > 0:
        s += num % 10
        num //= 10

    return s
