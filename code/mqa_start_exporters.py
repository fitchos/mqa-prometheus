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
This module provides a utility to start a list of exporters
for the MQ Appliance.
"""

import argparse
import csv
import shlex
import subprocess
import sys

from mqalib import get_password
from mqalib import get_version
from mqalib import resolve_directory


def main():

    # Build parser to handle the command line options
    parser = argparse.ArgumentParser(description='MQ Appliance Prometheus Exporter Start Utility - ' + get_version())
    parser.add_argument('-d', '--directory', type=str, required=False, default='', help = 'Path to directory for log and PID files (defaults to current directory)')
    parser.add_argument('-f', '--file',  type=str, required=True, help = 'Name of the file with the exporters configuration (CSV)') 
    parser.add_argument('-ln', '--lognumbers', type=int, required=False, default=10, help = 'Number of logs in a rotation (defaults to 10)')
    parser.add_argument('-ls', '--logsize', type=int, required=False, default=10485760, help = 'Size of logs in bytes (defaults to 10MB - 10485760)')
    parser.add_argument('-u', '--user', type=str, required=True, help = 'User to login to the appliance')
    parser.add_argument('-x', '--pw', type=str, required=False, help = 'Password to login to the appliance')

    # Display usage if needed
    if len(sys.argv) < 3:
       parser.print_help(sys.stderr)
       sys.exit(1)

    # Process command line options
    args = parser.parse_args()
    args.directory = resolve_directory(args)

    # Prompt for the password
    if args.pw == None:
        args.pw = get_password()

    print('MQ Appliance Prometheus Exporter Start Utility - ' + get_version())

    # Process the exporters configuration file (CSV)
    with open(args.file) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')

        exporter_count = 0
        for exporter in csvreader:
            command = shlex.split('python mqa_metrics.py -a ' + exporter[0] + 
                                                       ' -i ' + exporter[1] + 
                                                       ' -p ' + exporter[2] + 
                                                       ' -l ' + args.directory + exporter[0] + '_exporter.log' +  
                                                       ' -ls ' + str(args.logsize) + 
                                                       ' -ln ' + str(args.lognumbers) + 
                                                       ' -u ' + args.user + 
                                                       ' -x ' + args.pw + 
                                                       ' -hp ' + exporter[3] + 
                                                       ' -t ' + exporter[4])                    
            
            # Start the exporter
            process = subprocess.Popen(command)
            print('Started exporter for appliance \'' + exporter[0] + '\' on HTTP port ' + str(exporter[3]) + ', PID is ' + str(process.pid))

            # Write pid of the exporter to file
            with open(args.directory + exporter[0] + '.pid', 'w') as pidfile:
                pidfile.write(str(process.pid))

            exporter_count += 1

        print('Started ' + str(exporter_count) + ' exporter(s).')

if __name__ == '__main__':
    main()
