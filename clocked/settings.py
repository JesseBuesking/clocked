""" Various configuration properties. """


from clocked.profiler_provider import ProfilerProvider
from clocked.stopwatch import StopWatch


class Settings(object):
    """ Various configuration properties. """

    _profiler_provider = None

    @classmethod
    def ensure_profiler_provider(cls):
        """
        Makes sure that there's a profiler provider.
        """
        if cls._profiler_provider is None:
            cls._profiler_provider = ProfilerProvider()

    @classmethod
    def stopwatch_provider(cls):
        """
        Provides a stopwatch.
        """
        sw = StopWatch()
        sw.start()
        return sw
