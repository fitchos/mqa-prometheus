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
This module provides the ability to start a list of exporters
for the MQ Appliance.
"""

import argparse
import csv
import shlex
import subprocess
import sys

from getpass import getpass
from mqalib import get_password


def main():

    # Build parser to handle the command line options
    parser = argparse.ArgumentParser(description='MQ Appliance Prometheus Exporter Start Utility')
    parser.add_argument('-f', '--file',  type=str, required=True, help = 'Name of the file with the exporters configuration (CSV)') 
    parser.add_argument('-lp', '--logpath', type=str, required=False, default='', help = 'Directory path to store log and PID files (defaults to current directory')
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

    args.logpath = args.logpath.replace('\\', '/')

    # Prompt for the password
    if args.pw == None:
        args.pw = get_password()

    print('MQ Appliance Prometheus Exporter Start Utility')

    # Process the exporters configuration file (CSV)
    with open(args.file) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        linecount = 0
        for row in csvreader:
            command = shlex.split('python mqa_metrics.py -a ' + row[0] + 
                                                       ' -i ' + row[1] + 
                                                       ' -p ' + row[2] + 
                                                       ' -l ' + args.logpath + row[0] + '_exporter.log' +  
                                                       ' -ls ' + str(args.logsize) + 
                                                       ' -ln ' + str(args.lognumbers) + 
                                                       ' -u ' + args.user + 
                                                       ' -x ' + args.pw + 
                                                       ' -hp ' + row[3] + 
                                                       ' -t ' + row[4])                    
            
            process = subprocess.Popen(command)
            print('Started exporter for appliance \'' + row[0] + '\' on HTTP port ' + str(row[3]) + ', PID is ' + str(process.pid))

            # Write pid to file
            with open(args.logpath + row[0] + '.pid', 'w') as pidfile:
                pidfile.write(str(process.pid))

            linecount += 1

        print('Started ' + str(linecount) + ' exporters.')

if __name__ == '__main__':
    main()
