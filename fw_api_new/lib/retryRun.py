# -*- coding = UTF-8 -*-
import sys
import functools
import traceback
import inspect

class Retry(object):
    def __new__(cls, func_or_cls=None, max_n=1, func_prefix="test"):
        self = object.__new__(cls)
        if func_or_cls:
            self.__init__(func_or_cls, max_n, func_prefix)
            return self(func_or_cls)
        else:
            return self

    def __init__(self, func_or_cls=None, max_n=1, func_prefix="test"):
        self._prefix = func_prefix
        self._max_n = max_n

    def __call__(self, func_or_cls=None):
        if inspect.isfunction(func_or_cls):
            @functools.wraps(func_or_cls)
            def wrapper(*args, **kwargs):
                n = 0
                while n <= self._max_n:
                    try:
                        n += 1
                        func_or_cls(*args, **kwargs)
                        return
                    except Exception:  # 可以修改要捕获的异常类型
                        if n <= self._max_n:
                            trace = sys.exc_info()
                            traceback_info = str()
                            for trace_line in traceback.format_exception(trace[0], trace[1], trace[2], 3):
                                traceback_info += trace_line
                            print(traceback_info)  # 输出组装的错误信息
                            args[0].tearDown()
                            args[0].setUp()
                        else:
                            raise

            return wrapper
        elif inspect.isclass(func_or_cls):
            for name, func in list(func_or_cls.__dict__.items()):
                if inspect.isfunction(func) and name.startswith(self._prefix):
                    setattr(func_or_cls, name, self(func))
            return func_or_cls
        else:
            raise AttributeError