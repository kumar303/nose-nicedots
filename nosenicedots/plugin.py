
import inspect
from inspect import isfunction
import logging
import os
import unittest
from unittest import TestResult, _TextTestResult
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
        # TODO(Kumar) this will break when unittest changes.
        # Current code is from 2.6

        # Don't repeat failures at the bottom? Hmm.

        # def printErrors():
        #     # We already printed errors:
        #     self.stream.writeln("")
        #
        # result.printErrors = printErrors

        nice_result = NiceDotsResult(self.runner.stream,
                                     self.runner.descriptions,
                                     self.runner.verbosity)

        # Monkey patch unittest result with a custom result.
        # This is because Nose cannot completely replace the
        # unittest result.  Without this we can replace a few things.
        for fn in nice_result.__class__.__dict__:
            setattr(result, fn, getattr(nice_result, fn))

        # Reference some attributes so that summaries work:
        for a in ('failures', 'errors', 'testsRun', 'shouldStop'):
            setattr(nice_result, a, getattr(result, a))

        # Tell other plugins that it's probably not safe to
        # do their own monkeypatching.
        return result

    def prepareTestRunner(self, runner):
        self.runner = runner


class NiceDotsResult(_TextTestResult):

    def getDescription(self, test):
        return nice_test_address(test)

    def printError(self, flavour, err, test):
        err = super(NiceDotsResult, self)._exc_info_to_string(err, test)
        self.stream.writeln("")
        self.stream.writeln(self.separator1)
        self.stream.writeln("%s: %s" % (flavour,
                                        self.getDescription(test)))
        self.stream.writeln(self.separator2)
        self.stream.writeln("%s" % err)

    def addError(self, test, err):
        exc, val, tb = err
        if not issubclass(exc, SkipTest):
            super(NiceDotsResult, self).addError(test, err)
        if self.showAll:
            self.stream.writeln("ERROR")
        elif self.dots:
            if issubclass(exc, SkipTest):
                self.stream.writeln("")
                self.stream.writeln("SKIP: %s" % nice_test_address(test))
            else:
                self.printError('ERROR', err, test)
                self.stream.flush()

    def addFailure(self, test, err):
        super(NiceDotsResult, self).addFailure(test, err)
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.printError('FAIL', err, test)
            self.stream.flush()

    def addSuccess(self, test):
        super(NiceDotsResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln("ok")
        elif self.dots:
            context = get_context(test)
            if context:
                self.stream.writeln("")
                self.stream.writeln(context)
            self.stream.write('.')
            self.stream.flush()


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
