
import sys
import unittest

import nose.case
from nose.failure import Failure
from nose.tools import eq_
from nose.pyversion import unbound_method

from nosenicedots import nice_test_address

class TestNiceAddresses(unittest.TestCase):

    def test_function(self):
        def func():
            pass

        case = nose.case.FunctionTestCase(func)
        eq_(nice_test_address(case),
            'nosenicedots/tests/test_units.py:func')

    def test_generator(self):
        def fn(x):
            pass
        def gen():
            yield fn, (1,)

        case = nose.case.FunctionTestCase(gen)
        eq_(nice_test_address(case),
            'nosenicedots/tests/test_units.py:gen')

    def test_method_unittest(self):
        class TC(unittest.TestCase):
            def test(self):
                pass

        eq_(nice_test_address(TC('test')),
            'nosenicedots/tests/test_units.py:TC.test')

        case = nose.case.Test(TC('test'))
        eq_(nice_test_address(case),
            'nosenicedots/tests/test_units.py:TC.test')

    def test_method_raw(self):
        class TC(object):
            def test(self):
                pass

        case = nose.case.MethodTestCase(unbound_method(TC, TC.test))
        eq_(nice_test_address(case),
            'nosenicedots/tests/test_units.py:TC.test')

    def test_method_gen(self):
        def fn(x):
            pass
        class TC(object):
            def test_gen(self):
                yield fn, (1,)

        case = nose.case.MethodTestCase(unbound_method(TC, TC.test_gen))
        eq_(nice_test_address(case),
            'nosenicedots/tests/test_units.py:TC.test_gen')

    def test_syntax_error(self):
        try:
            raise RuntimeError(
                    "more realistically this would be a SyntaxError")
        except:
            exc = sys.exc_info()
        case = Failure(exc[0], exc[1], tb=exc[2],
                       address=('some_file.py', None, None))
        eq_(nice_test_address(case), 'some_file.py')

    def test_catastropic_failure(self):
        try:
            raise RuntimeError("really big error")
        except:
            exc = sys.exc_info()
        case = Failure(exc[0], exc[1], exc[2], address=None)
        eq_(nice_test_address(case),
            '??')
