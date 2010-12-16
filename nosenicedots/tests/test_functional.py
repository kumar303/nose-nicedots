
import os
import unittest
import textwrap

from nose.plugins import PluginTester

from nosenicedots import NiceDots

class TestPluginFoo(PluginTester, unittest.TestCase):
    activate = '--with-nicedots'
    plugins = [NiceDots()]
    suitepath = os.path.join(os.path.dirname(__file__), 'example-suite')

    def test_foo(self):
        print self.output
        assert 'EF' in self.output
        assert './nosenicedots/tests/example-suite/test_stuff/test_classes.py:TestClass' in self.output
        assert '..' in self.output
        assert './nosenicedots/tests/example-suite/test_stuff/test_functions.py' in self.output
        assert '..FE' in self.output
        assert './nosenicedots/tests/example-suite/test_stuff/test_generators.py' in self.output

    def makeSuite(self):
        pass
