#!/usr/bin/env python

# Copyright 2021 Oliver "Fitch" Fisse (fitchos@protonmail.com)
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

"""
This module provides a utility to list the exporters currently running
for the MQ Appliance.
"""

import argparse
import errno
import glob
import os

from mqalib import get_version
from mqalib import resolve_directory


def main():

    # Build parser to handle the command line options
    parser = argparse.ArgumentParser(description='MQ Appliance Prometheus Exporter List Utility - ' + get_version())
    parser.add_argument('-a', '--appliance', type=str, required=False, default='*', help = 'Name of the appliance')
    parser.add_argument('-d', '--directory', type=str, required=False, default='', help = 'Path to directory for PID files (defaults to current directory)')

    # Process command line options
    args = parser.parse_args()
    args.directory = resolve_directory(args)

    print('MQ Appliance Prometheus Exporter List Utility - ' + get_version())

    # Search for exporters by looking at pid files
    exporter_count = 0
    for file in glob.glob(args.directory + args.appliance + '.pid'):
        with open(file, "r") as f:
            pid = f.readline()

        print('Exporter for appliance \'' + os.path.basename(os.path.splitext(file)[0]) + '\' is running with PID ' + pid)

        exporter_count += 1

    if exporter_count == 0:
        print('No exporter found or the specific exporter(s) are not running, or')
        print('you may be NOT be looking at the correct directory for the PID files!')
    else:
        print(str(exporter_count) + ' exporter(s) are currently running.')

if __name__ == '__main__':
    main()
