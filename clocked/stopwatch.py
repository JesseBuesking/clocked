"""
Altered from https://gist.github.com/sumeet/1123871
"""


import time


class StopWatch(object):
    """
    A stopwatch utility for timing execution that can be used as a regular
    object or as a context manager.

    NOTE: This should not be used an accurate benchmark of Python code, but a
    way to check how much time has elapsed between actions. And this does not
    account for changes or blips in the system clock.

    Instance attributes:
    start_time -- timestamp when the timer started
    stop_time -- timestamp when the timer stopped

    As a regular object:

    >>> stopwatch = StopWatch()
    >>> stopwatch.start()
    >>> time.sleep(.001)
    >>> 1 <= stopwatch.elapsed_milliseconds <= 2
    True
    >>> time.sleep(.001)
    >>> stopwatch.stop()
    >>> 2 <= stopwatch.elapsed_milliseconds
    True

    As a context manager:

    >>> with StopWatch() as stopwatch:
    ...     time.sleep(.001)
    ...     print repr(1 <= stopwatch.time_elapsed <= 2)
    ...     time.sleep(.001)
    True
    >>> 2 <= stopwatch.total_milliseconds
    True
    """

    def __init__(self):
        """Initialize a new `Stopwatch`, but do not start timing."""
        self.start_time = None
        self.stop_time = None

    def start(self):
        """Start timing."""
        self.start_time = time.clock()

    def stop(self):
        """Stop timing."""
        self.stop_time = time.clock()

    @property
    def elapsed_milliseconds(self):
        """
        Return the number of milliseconds that have elapsed since this
        `Stopwatch` started timing.

        This is used for checking how much time has elapsed while the timer is
        still running.
        """
        return (time.clock() - self.start_time) * 1000.0

    @property
    def total_milliseconds(self):
        """
        Return the number of milliseconds that elapsed from when this
        `Stopwatch` started to when it ended.
        """
        return (self.stop_time - self.start_time) * 1000.0

    def __enter__(self):
        """Start timing and return this `Stopwatch` instance."""
        self.start()
        return self

    def __exit__(self, _type, value, traceback):
        """Stop timing.

        If there was an exception inside the `with` block, re-raise it.

        >>> with StopWatch() as stopwatch:
        ...     raise Exception
        Traceback (most recent call last):
            ...
        Exception
        """
        self.stop()
        if _type:
            raise type, value, traceback
