""" Tests for Clocked. """


import timeit
import unittest
from clocked import cuuid
from clocked.clockit import Clocked
from clocked.decorators import clocked
from clocked.profiler_provider import ProfilerProvider
from clocked.settings import Settings


ITERATIONS = 300000


class TestClocked(unittest.TestCase):

    def _assert(self, mini, val, maxi):
        self.assertTrue(
            mini <= val <= maxi,
            '{} <= {} <= {} is not true'.format(
                mini,
                val,
                maxi
            )
        )

    def _with(self):
        @clocked
        def _test():
            # noinspection PyUnusedLocal
            s = "test"
        _test()

    def _without(self):
        def _test():
            # noinspection PyUnusedLocal
            s = "test"
        _test()

    def test_comparison_normal_uuid(self):
        cuuid.toggle_thread_unsafe_uuid(False)
        print('normal uuid')
        self._compare()
        print('')

    # def test_comparison_unsafe(self):
    #     cuuid.toggle_thread_unsafe_uuid(True)
    #     print('unsafe uuid')
    #     self._compare()
    #     print('')

    def _compare(self):
        without = self.get_without()
        with_off = self.get_with_off()
        with_on = self.get_with_on()

        print('without: {} ms ({} per ms; {} ms per)'.format(
            round(without * 1000.0, 2),
            round(ITERATIONS / (without * 1000.0), 2),
            round((without * 1000.0) / ITERATIONS, 4)
        ))
        print('with_off: {} ms ({} per ms; {} ms per)'.format(
            round(with_off * 1000.0, 2),
            round(ITERATIONS / (with_off * 1000.0), 2),
            round((with_off * 1000.0) / ITERATIONS, 4)
        ))
        print('with_on: {} ms ({} per ms; {} ms per)'.format(
            round(with_on * 1000.0, 2),
            round(ITERATIONS / (with_on * 1000.0), 2),
            round((with_on * 1000.0) / ITERATIONS, 4)
        ))
        print('ratios: {} -> {} -> {}'.format(
            round(with_on / without, 1),
            round(with_on / with_off, 1),
            '1'
        ))

    def get_without(self):
        t = timeit.Timer(self._without)
        t.timeit(ITERATIONS)
        elapsed = t.timer()
        return elapsed

    def get_with_off(self):
        Settings._profiler_provider = None
        ProfilerProvider._profiler = None
        t = timeit.Timer(self._with)
        t.timeit(ITERATIONS)
        elapsed = t.timer()
        return elapsed

    def get_with_on(self):
        Clocked.initialize('template')
        t = timeit.Timer(self._with)
        t.timeit(ITERATIONS)
        elapsed = t.timer()
        return elapsed
