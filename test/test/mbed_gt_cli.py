#!/usr/bin/env python
# Copyright (c) 2018, Arm Limited and affiliates.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import six
import sys
import unittest

from mbed_os_tools.test import mbed_greentea_cli
from mbed_os_tools.test.tests_spec import TestSpec

test_spec_def = {
    "builds": {
        "K64F-ARM": {
            "platform": "K64F",
            "toolchain": "ARM",
            "base_path": "./.build/K64F/ARM",
            "baud_rate": 115200,
            "tests": {
                "mbed-drivers-test-generic_tests":{
                    "binaries":[
                        {
                            "binary_type": "bootable",
                            "path": "./.build/K64F/ARM/mbed-drivers-test-generic_tests.bin"
                        }
                    ]
                },
                "mbed-drivers-test-c_strings":{
                    "binaries":[
                        {
                            "binary_type": "bootable",
                            "path": "./.build/K64F/ARM/mbed-drivers-test-c_strings.bin"
                        }
                    ]
                }
            }
        }
    }
}

class GreenteaCliFunctionality(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_local_host_tests_dir_invalid_path(self):
        test_path = mbed_greentea_cli.get_local_host_tests_dir("invalid-path")
        self.assertEqual(test_path, None)

    def test_get_local_host_tests_dir_valid_path(self):
        path = "."
        test_path = mbed_greentea_cli.get_local_host_tests_dir(path)
        self.assertEqual(test_path, path)

    def test_get_local_host_tests_dir_default_path(self):
        import os
        import shutil
        import tempfile

        curr_dir = os.getcwd()
        test1_dir = tempfile.mkdtemp()
        test2_dir = os.mkdir(os.path.join(test1_dir, "test"))
        test3_dir = os.mkdir(os.path.join(test1_dir, "test", "host_tests"))

        os.chdir(test1_dir)

        test_path = mbed_greentea_cli.get_local_host_tests_dir("")
        self.assertEqual(test_path, "./test/host_tests")

        os.chdir(curr_dir)
        shutil.rmtree(test1_dir)

    def test_create_filtered_test_list(self):
        test_spec = TestSpec()
        test_spec.parse(test_spec_def)
        test_build = test_spec.get_test_builds()[0]

        test_list = mbed_greentea_cli.create_filtered_test_list(test_build.get_tests(),
                                                                'mbed-drivers-test-generic_*',
                                                                None,
                                                                test_spec=test_spec)
        self.assertEqual(set(test_list.keys()), set(['mbed-drivers-test-generic_tests']))

        test_list = mbed_greentea_cli.create_filtered_test_list(test_build.get_tests(),
                                                                '*_strings',
                                                                None,
                                                                test_spec=test_spec)
        self.assertEqual(set(test_list.keys()), set(['mbed-drivers-test-c_strings']))

        test_list = mbed_greentea_cli.create_filtered_test_list(test_build.get_tests(),
                                                                'mbed*s',
                                                                None,
                                                                test_spec=test_spec)
        expected = set(['mbed-drivers-test-c_strings', 'mbed-drivers-test-generic_tests'])
        self.assertEqual(set(test_list.keys()), expected)

        test_list = mbed_greentea_cli.create_filtered_test_list(test_build.get_tests(),
                                                                '*-drivers-*',
                                                                None,
                                                                test_spec=test_spec)
        expected = set(['mbed-drivers-test-c_strings', 'mbed-drivers-test-generic_tests'])
        self.assertEqual(set(test_list.keys()), expected)

if __name__ == '__main__':
    unittest.main()
