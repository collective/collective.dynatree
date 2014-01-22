# -*- coding: utf-8 -*-

from interlude import interact

import doctest
import os
import pprint
import unittest

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS


TESTFILES = [
    'utils.rst',

]


def test_suite():
    return unittest.TestSuite([
        doctest.DocFileSuite(
            filename,
            optionflags=optionflags,
            globs={
                'interact': interact,
                'pprint': pprint.pprint,
            },
        ) for filename in TESTFILES])
