==============================
Nice Dots
==============================

It's a nosetests_ plugin that prints nicer dots grouped by class/module.

.. _nosetests: http://somethingaboutorange.com/mrl/projects/nose/

Install
=======

From PyPI::

  pip install nosenicedots

or from source::

  pip install -e git+git://github.com/kumar303/nose-nicedots.git#egg=nosenicedots

Usage
=====

::

  nosetests --with-nicedots

Example
=======

::

  $ nosetests --with-nicedots

  apps/devhub/tests/test_views.py:TestActivity
  ..............
  apps/devhub/tests/test_views.py:TestAddVersion
  .
  ======================================================================
  FAIL: apps/devhub/tests/test_views.py:TestAddVersion.test_unique_version_num
  ----------------------------------------------------------------------
  Traceback (most recent call last):
    File "/path/to/apps/devhub/tests/test_views.py", line 3132, in test_unique_version_num
      assert 0
  AssertionError


  apps/devhub/tests/test_views.py:TestCreateFoobar
  ..
  apps/devhub/tests/test_views.py:TestDashboard
  .....
  apps/devhub/tests/test_views.py:TestDelete
  ..
  ======================================================================
  FAIL: apps/devhub/tests/test_views.py:TestAddVersion.test_unique_version_num
  ----------------------------------------------------------------------
  Traceback (most recent call last):
    File "/path/to/apps/devhub/tests/test_views.py", line 3132, in test_unique_version_num
      assert 0
  AssertionError

  ----------------------------------------------------------------------
  Ran 44 tests in 1.62s

  FAILED (failures=1)

This new style of output is intended as a more useful test report and is
inspired by `py.test`_. Instead of a confusing (yet pretty) mess of dots
you'll see a printout of the module or class followed by dots that indicate
each test in that group.

You'll see the traceback for a failure immediately, which was designed for
long running test suites. Note that the tracebacks are repeated again down at
the bottom in case the output had scrolled off the screen already. Using
``--stop`` will not duplicate failure output.

.. _`py.test`: http://pytest.org/

It's Also A Test Address
========================

Each module or class group also doubles as an argument you can give to Nose if
you want to re-run that group of tests. From the above output you could
copy/paste and re-run tests in the TestActivity class like this::

  $ nosetests --with-nicedots apps/devhub/tests/test_views.py:TestActivity

  apps/devhub/tests/test_views.py:TestActivity
  ..............
  ----------------------------------------------------------------------
  Ran 14 tests in 0.62s

  OK

Caveats
=======

- If any other plugin needs to patch the unittest result then it will
  conflict with Nice Dots.
- Python 2.5, 2.6 and 2.7 are supported at the moment. Other versions may or
  may not work.  Python 3 is **not** yet supported.  There are a few failing
  tests.
