Clocked
=======

A library to enable easier profiling, based _**loosely**_ on
[MiniProfiler](http://miniprofiler.com/). For a more full-featured
implementation for use in web development, check out the [GAE Mini Profiler]
(https://github.com/Khan/gae_mini_profiler). This library is meant to be more
lightweight than a full MiniProfiler implementation so that you can quickly
load it into a project and start timing things.

Use Case
========
I was looking to profile some code and came across [this blog post]
(http://www.huyng.com/posts/python-performance-analysis/) that covers things
quite nicely. However, the coarse and fine grain timing sections leaves a lot
up to reader and aren't very robust, so this library is meant to fill the gap.

This library is meant to be used to do higher-level profiling,
where you litter your code with profiling statements and generate a report to
quickly find where your code is spending all of it's time. From there,
fall back to tools like [timeit](https://docs.python.org/2/library/timeit
.html) or [line_profiler](https://github.com/rkern/line_profiler).

To start, initialize the session by calling

```python
Clocked.initialize('at the root scope!')
```

Then run your code with ``clocked`` decorators and/or ``with Clocked``
statements. At the end of the session, output a report with either
``Clocked.verbose_report()`` or ``Clocked.hotspot_report()`` to see some
timing information.

Supported ways to decorate
--------------------------

#### class level

```python
@clocked
class MyClass(object):

  def will_be_timed_one(self):
    ...

  def will_be_timed_two(self):
    ...

```

#### function level

```python
class MyClass(object):

  @clocked
  def will_be_timed(self):
    ...

  def will_not_be_timed(self):
    ...

```

Decorators aren't specific to classes, so you can apply them to individual
functions like so

```python
@clocked
def some_function():
  ...
```

How to use inline
-----------------

You can use the Clocked object to time something without using a decorator

```python
with Clocked("i'm timing this!"):
  ...
```

Generate a report
-----------------

To get at the timing information, the simplest thing to do is generate a report

```python
>>> Clocked.verbose_report()
"""
All timing information:
-----------------------
test raw simple (326.5 ms)
 loop 1 (326.5 ms)
"""
>>> Clocked.hotspot_report()
"""
Hotspots:
---------
loop 4 (164.5 ms [19.9, 22.0], 8 hits)
loop 3 (160.8 ms [19.9, 20.9], 8 hits)
loop 2 (1.0 ms [0.2, 0.3], 4 hits)
loop 1 (0.2 ms [0.2, 0.2], 1 hits)
test raw simple (0.0 ms [0.0, 0.0], 1 hits)
"""
```

Performance
-----------

To improve performance when testing single-threaded applications,
enable faster uuid generation by turning on thread unsafe uuid generation with
``clocked.cuuid.toggle_thread_unsafe_uuid(True)``
