
from nose.exc import SkipTest

def test_one():
    pass

def test_two():
    pass

def test_failing():
    assert 0

def test_error():
    raise RuntimeError

def test_skip():
    raise SkipTest("skipped")
