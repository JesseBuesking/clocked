

import sys
from clocked.profiler import Profiler
from clocked.settings import Settings


class Clocked(object):
    """
    An object to track timing information.

    Based on MiniProfilerExtensions.cs
    """

    @classmethod
    def initialize(cls, session_name):
        """
        Initializes the underlying timer.

        :param str session_name: the name for this session
        """
        Settings.ensure_profiler_provider()
        Settings.profiler_provider.start(session_name)

    def __init__(self, name):
        self._name = name

    def __enter__(self):
        """
        Equivalent to Step.
        """
        profiler = Profiler.current()
        if profiler is None:
            return None
        else:
            return profiler.step_impl(self._name)

    # noinspection PyUnusedLocal
    def __exit__(self, _type, value, traceback):
        """
        End profiling step timing.

        If there was an exception inside the `with` block, re-raise it.
        """
        profiler = Profiler.current()
        if profiler is not None:
            profiler.head.stop()

        if _type:
            # re-raise any exceptions
            raise

    @classmethod
    def get(cls, name):
        """
        Returns a generator for all timing information by name.

        :param str name: the name to get
        """
        profiler = Profiler.current()
        for timing in profiler.get_timing_hierarchy():
            if timing.name != name:
                continue

            yield timing

    @classmethod
    def verbose_report(cls, output_method=None):
        """
        Prints a report of the timing information. This report is
        hierarchical with indentation being used to represent function nesting.

        :param func output_method: a method that takes a string and manages
         where the output goes, defaulting to print
        """
        if output_method is None:
            def p(x):
                print(x)
            output_method = p

        profiler = Profiler.current()

        def _print(timing, depth=0):
            if timing.duration_milliseconds is None:
                dm = profiler.get_duration_milliseconds(
                    timing.start_milliseconds
                )
            else:
                dm = timing.duration_milliseconds

            output_method(depth * ' ' + '{} ({} ms)'.format(
                timing.name,
                round(dm, 1)
            ))
            if timing.has_children:
                for child in timing.children:
                    _print(child, depth + 1)

        header = 'All timing information:'

        output_method('')
        output_method(header)
        output_method('-' * len(header))
        _print(profiler.root, 0)

    @classmethod
    def hotspot_report(cls, output_method=None, limit=None):
        """
        Creates a hotspot report and sends it to a target output.

        The format of the output is:
          name (total function time [min, max], number of hits)

        Where total function time is the aggregated total time of the function
        minus the aggregated total times of all functions beneath that are
        being profiled.

        :param func output_method: a method that takes a string and manages
         where the output goes, defaulting to print
        :param int limit: used to limit the output to the top n culprits
        """
        if output_method is None:
            def p(x):
                print(x)
            output_method = p

        header = 'Hotspots:'

        output_method('')
        output_method(header)
        output_method('-' * len(header))

        for name, ms, min_ms, max_ms, hits in cls.generate_hotspots(limit):
            output_method(
                '{} ({} ms [{}, {}], {} hits)'.format(
                    name, ms, min_ms, max_ms, hits
                )
            )

    @classmethod
    def generate_hotspots(cls, limit=None):
        """
        Generates hotspots in decreasing order of badness.

        :param int limit: used to limit the results to the top n culprits
        :returns: generator for top hotspots
        :rtype: generator of (name, total ms, min ms, max ms, number of hits)
        """
        aggregates = dict()

        def _agg(timing, depth=0):
            dm = max(timing.duration_without_children_milliseconds(), 0.0)

            if timing.name not in aggregates:
                aggregates[timing.name] = (0.0, sys.maxint, 0.0, 0)

            tup = aggregates[timing.name]
            aggregates[timing.name] = (
                tup[0] + dm,
                min(tup[1], dm),
                max(tup[2], dm),
                tup[3] + 1
            )
            if timing.has_children:
                for child in timing.children:
                    _agg(child, depth + 1)

        profiler = Profiler.current()

        _agg(profiler.root, 0)

        tups = [i for i in aggregates.iteritems()]
        tups.sort(key=lambda x: x[1][0], reverse=True)

        maxi = limit if limit is not None else sys.maxint
        for idx, tup in enumerate(tups):
            if idx >= maxi:
                break

            yield tup[0], tup[1][0], tup[1][1], tup[1][2], tup[1][3]
