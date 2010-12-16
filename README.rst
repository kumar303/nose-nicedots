==============================
Nice Dots
==============================

Prints module/class name then dots for nosetests_.

.. _nosetests: http://somethingaboutorange.com/mrl/projects/nose/

Install
=======

  pip install -e git+git...#egg=nosenicedots

Usage
=====
  
  nosetests --with-nicedots

Example
=======

::
  
  $ nosetests --with-nicedots
  ./yourapp/tests/test_models.py:FooBarTest
  ...
  ./yourapp/tests/test_models.py:BarBarTest
  ............FFE......F
  ./yourapp/tests/test_helpers.py
  .....
