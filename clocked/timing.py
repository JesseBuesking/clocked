"""
An individual profiling step that can contain child steps.
"""


import cuuid


class Timing(object):
    """ An individual profiling step that can contain child steps. """

    __slots__ = ('id', 'parent_timing', 'profiler', 'parent', 'name', 'start',
                 'min_save_ms', 'include', 'include_children_with_min_save',
                 'start_milliseconds', 'children', 'custom_timings',
                 'duration_milliseconds')

    def __init__(self, profiler, parent, name, min_save_ms=None,
                 include_children_with_min_save=False):
        self.id = cuuid.uuid1()
        self.parent_timing = None
        self.profiler = profiler
        self.profiler.head = self

        if parent is not None:
            # root will have no parent
            parent.add_child(self)

        self.name = name
        self.start = profiler.elapsed_milliseconds
        self.min_save_ms = min_save_ms
        self.include_children_with_min_save = include_children_with_min_save
        self.start_milliseconds = self.start
        self.children = None
        self.custom_timings = None
        self.duration_milliseconds = None

    def has_custom_timings(self):
        """
        Returns true when there exists any CustomTiming objects in this
        CustomTimings.
        """
        if self.custom_timings is None:
            return False

        for value in self.custom_timings.values():
            if value is not None:
                return True

        return False

    @property
    def has_children(self):
        """
        Gets a value indicating whether this timing has inner timing steps.
        """
        return self.children is not None and 0 < len(self.children)

    @property
    def is_root(self):
        """
        Gets a value indicating whether this timing is the first one created
        in a session.
        """
        return self == self.profiler.root

    def duration_without_children_milliseconds(self):
        """
        Gets the elapsed milliseconds in this step without any children's
        durations.
        """
        result = self.duration_milliseconds
        if result is None:
            result = 0.0

        if self.has_children:
            for child in self.children:
                cm = child.duration_milliseconds
                if cm is None:
                    cm = 0.0

                result -= cm

        return round(result, 1)

    def depth(self):
        """
        Gets a value indicating how far away this timing is from the
        profiler's root.
        """
        result = 0
        parent = self.parent_timing

        while parent is not None:
            parent = parent.parent_timing
            result += 1

        return result

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Timing) and self.id == other.id

    def stop(self):
        """
        Completes this Timing's duration and sets the head up one level.
        """
        if self.duration_milliseconds is not None:
            return

        self.duration_milliseconds = self.profiler.get_duration_milliseconds(
            self.start_milliseconds
        )

        self.profiler.head = self.parent_timing

        has_msm = self.min_save_ms is not None and self.min_save_ms > 0
        if has_msm and self.parent_timing is not None:
            if self.include_children_with_min_save:
                compare_ms = self.duration_milliseconds
            else:
                compare_ms = self.duration_without_children_milliseconds()

            if compare_ms < self.min_save_ms:
                self.parent_timing.remove_child(self)

    def add_child(self, timing):
        """
        Add the parameter 'timing' to this Timing's Children collection.

        :param Timing timing: the timing to add
        """
        if self.children is None:
            self.children = []

        self.children.append(timing)
        timing.parent_timing = self

    def remove_child(self, timing):
        """
        Remove the 'timing' from this Timing's Children collection.

        :param Timing timing: the timing to remove
        """
        if self.children is not None:
            self.children.remove(timing)

    def add_custom_timing(self, category, custom_timing):
        """
        Adds a custom timing to this Timing step's dictionary of custom
        timings.

        :param str category: the kind of custom timings, e.g. "sql", "redis"
        :param Timing custom_timing: the custom timing
        """
        self.get_custom_timing_list(category).append(custom_timing)

    def remove_custom_timing(self, category, custom_timing):
        """
        Removes a custom timing from this Timing step's dictionary of custom
        timings.

        :param str category: the kind of custom timings, e.g. "sql", "redis"
        :param Timing custom_timing: the custom timing
        """
        self.get_custom_timing_list(category).remove(custom_timing)

    def get_custom_timing_list(self, category):
        """
        Returns the custom timing list keyed to the category, creating any
        collections when None.

        :param str category: the kind of custom timings, e.g. "sql", "redis"
        """
        if self.custom_timings is None:
            self.custom_timings = dict()

        result = self.custom_timings.get(category, [])
        self.custom_timings[category] = result

        return result
