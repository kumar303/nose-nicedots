
import os
import unittest
import textwrap

from nose.plugins import PluginTester
from nose.tools import eq_

from nosenicedots import NiceDots

def str_count(lines, chunk):
    count = 0
    for line in lines:
        if chunk in line:
            count += 1
    return count

class TestPluginFoo(PluginTester, unittest.TestCase):
    activate = '--with-nicedots'
    plugins = [NiceDots()]
    suitepath = os.path.join(os.path.dirname(__file__), 'example-suite')

    def test_foo(self):
        print '>' * 80
        print self.output
        print '>' * 80
        assert ('ERROR: nosenicedots/tests/example-suite/test_stuff/'
                'test_classes.py:TestClass.test_error') in self.output
        assert ('FAIL: nosenicedots/tests/example-suite/test_stuff/'
                'test_classes.py:TestClass.test_failing') in self.output
        assert ('nosenicedots/tests/example-suite/test_stuff/'
                'test_classes.py:TestClass') in self.output
        assert '..' in self.output
        assert ('nosenicedots/tests/example-suite/test_stuff/'
                'test_functions.py') in self.output
        assert '..' in self.output
        assert ('FAIL: nosenicedots/tests/example-suite/test_stuff/'
                'test_functions.py:test_failing') in self.output
        assert ('ERROR: nosenicedots/tests/example-suite/test_stuff/'
                'test_functions.py:test_error') in self.output
        assert ('SKIP: nosenicedots/tests/example-suite/test_stuff/'
                'test_functions.py:test_skip') in self.output
        assert ('nosenicedots/tests/example-suite/test_stuff/'
                'test_generators.py') in self.output
        # The summaries should be better:
        assert ('FAIL: test_stuff.test_functions'
                '.test_failing') not in self.output
        # First for the early error, secondly for the summary:
        eq_(str_count(self.output,
                      'FAIL: nosenicedots/tests/example-suite/test_stuff/'
                      'test_classes.py:TestClass.test_failing'),
            2)

    def makeSuite(self):
        pass
