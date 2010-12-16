
import inspect
from inspect import isfunction
import logging
import os
import unittest
from unittest import TestResult
import threading

from nose.plugins import Plugin
from nose.exc import SkipTest
from nose.case import Test, FunctionTestCase
from nose.util import isclass, isgenerator, ispackage, test_address

log = logging.getLogger('nose.plugins.nicedots')

hub = threading.local()
hub.last_context = None

class NiceDots(Plugin):
    """Prints module/class name then dots."""
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
        self = result # for monkeypatching! (see below)

        # TODO(Kumar) this will break when unittest changes.
        # Current code is from 2.6

        def printError(flavour, err, test):
            err = TestResult._exc_info_to_string(self, err, test)
            self.stream.writeln("")
            self.stream.writeln(self.separator1)
            self.stream.writeln("%s: %s" % (flavour, nice_test_address(test)))
            self.stream.writeln(self.separator2)
            self.stream.writeln("%s" % err)

        def addError(test, err):
            exc, val, tb = err
            if not issubclass(exc, SkipTest):
                TestResult.addError(self, test, err)
            if self.showAll:
                self.stream.writeln("ERROR")
            elif self.dots:
                if issubclass(exc, SkipTest):
                    self.stream.writeln("")
                    self.stream.writeln("SKIP: %s" % nice_test_address(test))
                else:
                    printError('ERROR', err, test)
                    self.stream.flush()

        result.addError = addError

        def addFailure(test, err):
            TestResult.addFailure(self, test, err)
            if self.showAll:
                self.stream.writeln("FAIL")
            elif self.dots:
                printError('FAIL', err, test)
                self.stream.flush()

        result.addFailure = addFailure

        def addSuccess(test):
            TestResult.addSuccess(self, test)
            if self.showAll:
                self.stream.writeln("ok")
            elif self.dots:
                context = get_context(test)
                if context:
                    self.stream.writeln("")
                    self.stream.writeln(context)
                self.stream.write('.')
                self.stream.flush()

        result.addSuccess = addSuccess

        # Don't repeat failures at the bottom? Hmm.

        # def printErrors():
        #     # We already printed errors:
        #     self.stream.writeln("")
        #
        # result.printErrors = printErrors


def nice_test_address(test):
    path, module, test_path = test_address(test)
    return "%s:%s" % (nice_path(path), test_path)

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
    path = os.path.abspath(path)
    if path.startswith(os.getcwd()):
        path = path.replace(os.getcwd(), '')[1:] # remove slash
    if path.endswith('.pyc'):
        path = path[0:-1]
    return path
