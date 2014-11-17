""" Decorator support for clocked. """


import inspect
import new
from clocked.profiler_provider import ProfilerProvider


def _create_function_wrapper(obj, name):
    def wrapper(*args, **kwargs):
        profiler = ProfilerProvider.get_current_profiler()
        if profiler is None:
            return obj(*args, **kwargs)
        else:
            profiler.step_impl(name)
            ret = obj(*args, **kwargs)
            profiler.head.stop()
            return ret

    wrapper.__module__ = obj.__module__
    wrapper.__name__ = obj.__name__
    wrapper.__doc__ = obj.__doc__
    wrapper.__dict__.update(getattr(obj, '__dict__', {}))
    return wrapper


def _create_method_wrapper(obj, name):
    if obj.im_self is not None:
        def wrapper(*args, **kwargs):
            profiler = ProfilerProvider.get_current_profiler()
            if profiler is None:
                return obj.__func__(*args, **kwargs)
            else:
                profiler.step_impl(name)
                ret = obj.__func__(*args, **kwargs)
                profiler.head.stop()
                return ret

        wrapper.__module__ = obj.__func__.__module__
        wrapper.__name__ = obj.__func__.__name__
        wrapper.__doc__ = obj.__func__.__doc__
        wrapper.__dict__.update(getattr(obj.__func__, '__dict__', {}))
        wrapper = new.instancemethod(wrapper, obj.im_self)
    else:
        def wrapper(*args, **kwargs):
            profiler = ProfilerProvider.get_current_profiler()
            if profiler is None:
                return obj.__func__(*args, **kwargs)
            else:
                profiler.step_impl(name)
                ret = obj.__func__(*args, **kwargs)
                profiler.head.stop()
                return ret

        wrapper.__module__ = obj.__func__.__module__
        wrapper.__name__ = obj.__func__.__name__
        wrapper.__doc__ = obj.__func__.__doc__
        wrapper.__dict__.update(getattr(obj.__func__, '__dict__', {}))

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
        return _create_function_wrapper(obj, '{}.{}:{}'.format(
            obj.__module__,
            obj.__name__,
            obj.func_code.co_firstlineno
        ))
    elif _is_class:
        for name, method in inspect.getmembers(obj):
            if inspect.isfunction(method):
                wrapper = _create_function_wrapper(method, '{}.{}.{}:{}'.format(
                    obj.__module__,
                    obj.__name__,
                    method.__name__,
                    method.func_code.co_firstlineno
                ))
                staticmethod(wrapper)
                setattr(obj, name, staticmethod(wrapper))
            elif inspect.ismethod(method):
                wrapper = _create_method_wrapper(method, '{}.{}.{}:{}'.format(
                    obj.__module__,
                    obj.__name__,
                    method.__func__.__name__,
                    method.func_code.co_firstlineno
                ))
                setattr(obj, name, wrapper)

    return obj
