""" Encapsulates logic for the profiler object. """


from clocked.settings import Settings
from clocked.timing import Timing


class Profiler(object):
    """
    A single profiler can be used to represent any number of steps/levels in
    a call-graph, via step().
    """

    def __init__(self, name):
        from datetime import datetime
        import uuid
        self.id = uuid.uuid1()
        self.started = datetime.utcnow()
        self._sw = Settings.stopwatch_provider()
        self._head = None
        self.set_root(Timing(self, None, name))

    @property
    def head(self):
        """
        Gets the head.
        """
        return self._head

    @head.setter
    def head(self, head):
        """
        Sets the head.

        :param head: the head item
        """
        self._head = head

    def get_root(self):
        """
        Gets the root timing.
        """
        return self._root

    def set_root(self, root):
        """
        Sets the root timing.

        :param Timing root: the root timing object
        """
        self._root = root
        self.root_timing_id = root.id

        if not self._root.has_children():
            return

        timings = [self._root]

        while 0 < len(timings):
            timing = timings.pop()

            if not timing.has_children():
                continue

            for i in range(len(timing.children)):
                timing.children[i].parent_timing = timing
                timings.append(timing.children[i])

    def elapsed_milliseconds(self):
        """
        Gets milliseconds that have elapsed.
        """
        return self._sw.elapsed_milliseconds

    def get_stopwatch(self):
        """
        Gets the underlying StopWatch.
        """
        return self._sw

    @classmethod
    def current(cls):
        """
        Gets the currently running Profiler; None if no Profiler was started.
        """
        Settings.ensure_profiler_provider()
        return Settings._profiler_provider.get_current_profiler()

    def start(self, session_name=None):
        """
        Starts a Profiler based on the current ProfilerProvider. This new
        profiler can be accessed by 'current'.

        :param str session_name: an optional name to give to the session
        """
        Settings.ensure_profiler_provider()
        return Settings._profiler_provider.start(session_name)

    def stop(self):
        """
        Ends the current profiling session, if one exists.
        """
        Settings.ensure_profiler_provider()
        Settings._profiler_provider.stop()

    @classmethod
    def step_static(cls, name):
        """
        Returns a profiler provider that will time the code between its
        creation and disposal.

        :param str name: the name to use for the step
        """
        return cls.current().step(name)

    def __str__(self):
        if self.get_root() is not None:
            return '{} ({} ms)'.format(
                self.get_root().name,
                self.duration_milliseconds
            )
        else:
            return ''

    def __eq__(self, other):
        return isinstance(other, Profiler) and self.id == other.id

    def get_timing_hierarchy(self):
        """
        Walks the Timing hierarchy contained in this profiler, starting with
        root, and returns each Timing found.
        """
        timings = [self.get_root()]

        while 0 < len(timings):
            timing = timings.pop()
            yield timing

            if timing.has_children():
                for child in timing.children:
                    timings.append(child)

    def step_impl(self, name, min_save_ms=None,
                  include_children_with_min_save=False):
        """
        Implementation for timing an individual step.

        :param name:
        :param min_save_ms:
        :param include_children_with_min_save:
        """
        return Timing(
            self,
            self.head,
            name,
            min_save_ms,
            include_children_with_min_save
        )

    def stop_impl(self):
        """ Stops the Profiler (all Timings in the hierarchy). """
        if not self._sw.is_running:
            return False

        self._sw.stop()
        self.duration_milliseconds = self.elapsed_milliseconds()

        for timing in self.get_timing_hierarchy():
            timing.stop()

        return True

    def get_duration_milliseconds(self, start):
        """
        Gets the amount of time that has elapsed.

        :param float start: a millisecond offset
        """
        return self.elapsed_milliseconds() - start
