""" Tests for Clocked. """


from time import sleep
import unittest


# noinspection PyDocstring
from clocked.clockit import Clocked
from clocked.decorators import clocked


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

    def ten_ms(self):
        sleep(.01)

    # def template(self):
    #     Clocked.initialize('template')
    #     # time stuff
    #     with Clocked('a'):
    #         # time something
    #         pass
    #     # print report
    #     Profiler.print_hotspot_report()

    def test_raw_simple(self):
        """ Simple raw test using Clocked object. """
        Clocked.initialize('test raw simple')

        with Clocked('loop 1'):
            for i in range(4):
                with Clocked('loop 2'):
                    for j in range(2):
                        with Clocked('loop 3'):
                            for j in range(2):
                                self.ten_ms()
                    for j in range(2):
                        with Clocked('loop 4'):
                            for j in range(2):
                                self.ten_ms()

        expected_total_time = 320
        delta_upper_bound = 10

        Clocked.verbose_report()
        Clocked.hotspot_report()
        print('')

        total = 0.0
        for timing in Clocked.get('loop 3'):
            total += timing.duration_milliseconds
        d = delta_upper_bound / 2
        e = expected_total_time / 2
        self._assert(e - d, total, e + d)

        total = 0.0
        for timing in Clocked.get('loop 4'):
            total += timing.duration_milliseconds
        d = delta_upper_bound / 2
        e = expected_total_time / 2
        self._assert(e - d, total, e + d)

        total = 0.0
        for timing in Clocked.get('loop 2'):
            total += timing.duration_milliseconds
        d = delta_upper_bound
        e = expected_total_time
        self._assert(e - d, total, e + d)

    def test_raise(self):
        def raises():
            with Clocked('test exception'):
                raise ValueError('some value error')
        self.assertRaises(ValueError, raises)


# noinspection PyDocstring
class TestDecorators(unittest.TestCase):

    def _assert(self, mini, val, maxi):
        self.assertTrue(
            mini <= val <= maxi,
            '{} <= {} <= {} is not true'.format(
                mini,
                val,
                maxi
            )
        )

    def test_function_decorator(self):
        """ Tests the function decorator @clocked. """
        Clocked.initialize('test function decorator')

        to = TestDecorators.TestFunctionObj()
        to.delay_method()
        t = [i for i in Clocked.get('delay_method')]
        self.assertEqual(1, len(t))
        t = t[0]
        self._assert(20-2, t.duration_milliseconds, 20+2)

    # noinspection PyDocstring
    class TestFunctionObj(object):

        @classmethod
        @clocked
        def delay_method(cls):
            sleep(.02)

    def test_class_decorator(self):
        """ Tests the class decorator @clocked. """
        Clocked.initialize('test class decorator')

        to = TestDecorators.TestClassObj()
        to.delay_method()
        t = [i for i in Clocked.get('delay_method')]
        self.assertEqual(1, len(t))
        t = t[0]
        self._assert(20-2, t.duration_milliseconds, 20+2)

    # noinspection PyDocstring
    @clocked
    class TestClassObj(object):

        @classmethod
        def delay_method(cls):
            sleep(.02)

    def test_function_and_class_decorators(self):
        """ Tests applying both function and class decorators @clocked. """
        Clocked.initialize('test function and class decorators')

        to = TestDecorators.TestFunctionAndClassObj()
        to.delay_method()
        t = [i for i in Clocked.get('delay_method')]
        self.assertEqual(1, len(t))
        t = t[0]
        self._assert(20-2, t.duration_milliseconds, 20+2)

    # noinspection PyDocstring
    @clocked
    class TestFunctionAndClassObj(object):

        @classmethod
        @clocked
        def delay_method(cls):
            sleep(.02)
