
import inspect
from inspect import isfunction
import logging
import os
import unittest
from unittest import TestResult
import threading

from nose.plugins import Plugin
from nose.case import Test, FunctionTestCase
from nose.util import isclass, isgenerator, ispackage, test_address

log = logging.getLogger('nose.plugins.nicedots')

hub = threading.local()
hub.last_context = None

class NiceDots(Plugin):
    """Print modules/classes then dots."""
    name = 'nicedots'

    def options(self, parser, env=os.environ):
        super(NiceDots, self).options(parser, env=env)
        self.parser = parser

    def configure(self, options, conf):
        super(NiceDots, self).configure(options, conf)
        if not self.enabled:
            return
        self.options = options

    def prepareTestResult(self, result):

        def addSuccess(test):
            self = result
            TestResult.addSuccess(self, test)
            if self.showAll:
                self.stream.writeln("ok")
            elif self.dots:
                context = get_context(test)
                if context:
                    self.stream.write("\n%s\n" % context)
                self.stream.write('.')
                self.stream.flush()

        result.addSuccess = addSuccess


def get_context(test):
    new_context = None

    if hasattr(test, 'test'):
        test = test.test

    if isinstance(test, FunctionTestCase):
        context = nice_path(inspect.getfile(inspect.getmodule(test.test)))
    elif isinstance(test, unittest.TestCase):
        context = '%s:%s' % (nice_path(inspect.getfile(test.__class__)),
                             test.__class__.__name__)
    else:
        raise NotImplemented('Unsure how to get context from: %r' % test)

    if context != hub.last_context:
        new_context = context
    hub.last_context = context
    return new_context


def nice_path(path):
    path = path.replace(os.getcwd(), '.')
    if path.endswith('.pyc'):
        path = path[0:-1]
    return path
