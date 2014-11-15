""" Decorator support for clocked. """


import inspect
from clocked.clockit import Clocked


def _create_function_wrapper(obj):
    def wrapper(*args, **kwargs):
        with Clocked(obj.__name__):
            return obj(*args, **kwargs)
    return wrapper


def _create_method_wrapper(obj):
    def wrapper(*args, **kwargs):
        with Clocked(obj.__name__):
            return obj.__func__(*args, **kwargs)
    return wrapper


def clocked(obj):
    """
    Clocked decorator. Put this on a class or and individual function for it's
    timing information to be tracked.
    """

    _is_class = inspect.isclass(obj)
    _is_func = inspect.isfunction(obj)
    if not _is_class and not _is_func:
        raise Exception('unsupported type {}'.format(type(obj)))

    if _is_func:
        return _create_function_wrapper(obj)
    elif _is_class:
        for name, method in inspect.getmembers(obj, inspect.ismethod):
            if inspect.ismethod(method) or inspect.isfunction(method):
                wrapper = _create_method_wrapper(method)
                setattr(obj, name, wrapper)

    return obj
