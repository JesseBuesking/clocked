

class ProfilerProvider(object):
    """
    Mostly for unit testing and single-threaded apps, only allows for one
    instance of a Profiler to be the 'current' one.
    """

    _profiler = None

    @classmethod
    def get_current_profiler(cls):
        """ Gets the current profiler. """
        return cls._profiler

    @classmethod
    def start(cls, session_name=None):
        """
        Starts a new profiling session.

        :param str session_name: the name of the current session
        """
        from clocked.profiler import Profiler
        cls._profiler = Profiler(session_name)
        cls._profiler.is_active = True

    @classmethod
    def stop(cls):
        """ Stops the current profiling session. """
        if cls._profiler is not None:
            cls._profiler.stop_impl()
