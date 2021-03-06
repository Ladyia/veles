# -*- coding: utf-8 -*-
"""
.. invisible:
     _   _ _____ _     _____ _____
    | | | |  ___| |   |  ___/  ___|
    | | | | |__ | |   | |__ \ `--.
    | | | |  __|| |   |  __| `--. \
    \ \_/ / |___| |___| |___/\__/ /
     \___/\____/\_____|____/\____/

Created on Jun 9, 2014

███████████████████████████████████████████████████████████████████████████████

Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.

███████████████████████████████████████████████████████████████████████████████
"""


import numpy
import os
import struct
import sys
import tempfile
import unittest

from veles.__main__ import Main
import veles.prng as rnd
from veles.workflow import Workflow


class Test(unittest.TestCase):
    def setUp(self):
        self.main = Main(True, "workflow", "config")

    def testSeeding(self):
        _, fname = tempfile.mkstemp(prefix="veles-test-seed-")
        with open(fname, 'wb') as fw:
            for i in range(100):
                fw.write(struct.pack('i', i))
        self.main._seed_random(fname + ":100")
        state1 = numpy.random.get_state()
        arr1 = numpy.empty(100)
        rnd.get().fill(arr1)
        self.main._seed_random(fname + ":100")
        state2 = numpy.random.get_state()
        try:
            self.assertTrue((state1[1] == state2[1]).all())
            arr2 = numpy.empty(100)
            rnd.get().fill(arr2)
            self.assertTrue((arr1 == arr2).all())
        except AssertionError:
            os.remove(fname)
            raise

    def testRun(self):
        argv = sys.argv
        sys.argv = [argv[0], "-s", "-p", "", "-v", "debug", __file__, __file__]
        self.main = Main()
        self.main.run()
        self.assertTrue(Workflow.run_was_called)

    def test_format_decimal(self):
        fd = Main.format_decimal
        res = fd(1047151)
        self.assertEqual(res, "1 047 151")
        res = fd(45)
        self.assertEqual(res, "45")
        res = fd(145)
        self.assertEqual(res, "145")
        res = fd(1145)
        self.assertEqual(res, "1 145")
        res = fd(12345)
        self.assertEqual(res, "12 345")

    def testSetupLogging(self):
        # Multiple calls test
        self.main.setup_logging("debug")
        self.main.setup_logging("debug")


def run(load, main):
    wf, _ = load(Workflow)
    wf.end_point.link_from(wf.start_point)
    main()
    Workflow.run_was_called = True

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testSeeding']
    unittest.main()
