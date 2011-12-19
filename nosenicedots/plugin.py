
import inspect
from inspect import isfunction
import logging
import os
import unittest
from unittest import TestResult, _TextTestResult
import threading

import nose.suite
from nose.plugins import Plugin
from nose.exc import SkipTest
from nose.case import Test, FunctionTestCase
from nose.util import isclass, isgenerator, ispackage, test_address

log = logging.getLogger('nose.plugins.nicedots')

hub = threading.local()
hub.last_context = None

class NiceDots(Plugin):
    """Prints nicer dots grouped by class/module."""
    name = 'nicedots'

    def options(self, parser, env=os.environ):
        super(NiceDots, self).options(parser, env=env)
        self.parser = parser

    def configure(self, options, conf):
        super(NiceDots, self).configure(options, conf)
        if not self.enabled:
            return
        self.cmd_options = options
        self.config = conf

    def prepareTestResult(self, result):
        # TODO(Kumar) this will break when unittest changes.
        # Current code is from 2.6

        nice_result = NiceDotsResult(self.runner.stream,
                                     self.runner.descriptions,
                                     self.runner.verbosity,
                                     stopOnError=self.config.stopOnError)

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

    def __init__(self, stream, descriptions, verbosity, stopOnError=False):
        super(NiceDotsResult, self).__init__(stream, descriptions, verbosity)
        self.stopOnError = stopOnError

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

    def printErrors(self):
        if self.stopOnError:
            # No need to print the error again during summary
            self.stream.writeln("")
        else:
            super(NiceDotsResult, self).printErrors()

    def addError(self, test, err):
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
                self.printError('ERROR', err, test)
                self.stream.flush()

    def addFailure(self, test, err):
        TestResult.addFailure(self, test, err)
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.printError('FAIL', err, test)
            self.stream.flush()

    def addSkip(self, test, reason):
        self.stream.writeln("")
        self.stream.writeln("SKIP: %s" % nice_test_address(test))
        base = super(TestResult, self)
        if hasattr(base, 'addSkip'):
            base.addSkip(test, reason)

    def addSuccess(self, test):
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


def nice_test_address(test):
    if isinstance(test, nose.suite.ContextSuite):
        addr = test_address(test.context)
        if hasattr(test, 'error_context') and test.error_context:
            addr = list(addr)
            if addr[2]:
                # class
                addr[2] = '%s.%s' % (addr[2], test.error_context)
            else:
                # module
                addr[2] = test.error_context
    else:
        addr = test_address(test)
    if addr is None:
        return '??'
    path, module, test_path = addr
    path = nice_path(path)
    if test_path is None:
        return path
    return "%s:%s" % (path, test_path)

nice_test_address.__test__ = False # Not a test for Nose


def get_context(test):
    new_context = None

    if hasattr(test, 'test'):
        test = test.test

    if isinstance(test, FunctionTestCase):
        mod = inspect.getmodule(test.test)
        try:
            file_ = inspect.getfile(mod)
        except ValueError:
            # builtin object
            file_ = repr(mod)
        context = nice_path(file_)
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
    if path is None:
        return path
    path = os.path.abspath(path)
    try:
        wd = os.getcwd()
    except OSError:
        # I guess you did something stupid like delete the current directory.
        pass
    else:
        if path.startswith(wd):
            path = path.replace(wd, '')[1:] # shorten and remove slash
    if path.endswith('.pyc'):
        path = path[0:-1]
    return path
