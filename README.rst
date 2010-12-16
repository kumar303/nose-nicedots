==============================
Nice Dots
==============================

Prints module/class name then dots for nosetests_.

.. _nosetests: http://somethingaboutorange.com/mrl/projects/nose/

Install
=======

  pip install -e git+git://github.com/kumar303/nose-nicedots.git#egg=nosenicedots

Usage
=====

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
  Ran 24 tests in 1.62s

  FAILED (failures=1)

Caveats
=======

This will probably only work in Python 2.6!  That might be fixable by creating different result instances per version.

Known Issues
============

- SkipTest is not fully supported.  It kinda works.
