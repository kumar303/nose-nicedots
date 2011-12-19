import unittest

from nose.exc import SkipTest


class TestClass(unittest.TestCase):

    def test_one(self):
        pass

    def test_two(self):
        pass

    def test_failing(self):
        assert 0

    def test_error(self):
        raise RuntimeError

    def test_skip(self):
        raise SkipTest('skipped')
