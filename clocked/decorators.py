""" Decorator support for clocked. """


import inspect
from clocked.clockit import Clocked


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
        def wrapper(*args, **kwargs):
            with Clocked(obj.__name__):
                return obj(*args, **kwargs)
        return wrapper
    elif _is_class:
        for name, method in inspect.getmembers(obj, inspect.ismethod):
            if inspect.ismethod(method) or inspect.isfunction(method):
                def wrapper(*args, **kwargs):
                    with Clocked(method.__name__):
                        return method.__func__(*args, **kwargs)

                setattr(obj, name, wrapper)

    return obj
