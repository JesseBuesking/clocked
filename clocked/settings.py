""" Various configuration properties. """


from clocked.profiler_provider import ProfilerProvider
from clocked.stopwatch import StopWatch


class Settings(object):
    """ Various configuration properties. """

    profiler_provider = None

    @staticmethod
    def ensure_profiler_provider():
        """
        Makes sure that there's a profiler provider.
        """
        if Settings.profiler_provider is None:
            Settings.profiler_provider = ProfilerProvider()

    @staticmethod
    def stopwatch_provider():
        """
        Provides a stopwatch.
        """
        sw = StopWatch()
        sw.start()
        return sw
