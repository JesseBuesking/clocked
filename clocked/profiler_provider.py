

class ProfilerProvider(object):
    """
    Mostly for unit testing and single-threaded apps, only allows for one
    instance of a Profiler to be the 'current' one.
    """

    _profiler = None

    @staticmethod
    def get_current_profiler():
        """ Gets the current profiler. """
        return ProfilerProvider._profiler

    @staticmethod
    def start(session_name=None):
        """
        Starts a new profiling session.

        :param str session_name: the name of the current session
        """
        from clocked.profiler import Profiler
        profiler = Profiler(session_name)
        profiler.is_active = True
        ProfilerProvider._profiler = profiler
        return profiler

    @staticmethod
    def stop():
        """ Stops the current profiling session. """
        if ProfilerProvider._profiler is not None:
            ProfilerProvider._profiler.stop_impl()
