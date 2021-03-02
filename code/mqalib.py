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

"""This module provides various helper functions."""

import csv
import fnmatch
import glob
import json
import logging
import requests
import os
import time
import sys

from datetime import datetime
from getpass import getpass


def call_rest_api(api_call, ip, port, session, timeout):
    """Perform a REST API call"""

    logging.info('Performing REST API call to gather \'' + api_call + '\'...')
    try:
        response = session.get('https://' + ip + ':' + port + api_call, timeout=timeout)
        if response.status_code == 200:
            data = json.loads(response.text)

            if 'result' in data:
                logging.warning('REST API call to gather \'' + api_call  + '\' failed --> ' + data['result'])
                return ''
        else:
            logging.error('REST API call to gather \'' + api_call  + '\' failed --> HTTP status code is ' + str(response.status_code) + ' (' + response.reason + ')')
            return ''
    except requests.RequestException as err:
        logging.error('REST API call to gather \'' + api_call  + '\' failed --> ' + str(err))
        return ''

    logging.info('REST API call to gather \'' + api_call  + '\' completed.')

    return data   

def init_rest_api(ip, port, auth, timeout):

    requests.packages.urllib3.disable_warnings()

    session = requests.Session()
    session.auth = auth
    session.verify = False

    while True:
        try:
            response = session.get('https://' + ip + ':' + port + '/mgmt/status/', timeout=timeout)
            if response.status_code == 200:
                logging.info('Successfully connected to appliance at ' + ip + '(' + str(port) + ')')
                break
        except requests.RequestException as err:
            logging.error('Failed to connect to appliance at ' + ip + '(' + str(port) + '), error is: ' + str(err))
            logging.info('Retrying in 20 seconds...')
            time.sleep(20)

    return session

def get_password(prompt='password: '):
    """Get a password from the command line"""

    while True:
        try:
            pw = getpass(prompt)
            pw = pw.strip()
            if len(pw) > 0:
                break
        except Exception as e:
            print('Error occurred while getting password: ' + str(e))
            sys.exit(1)

    return pw

def get_pid_file_list(file, directory, appliance):
    """Get a list of PID files"""

    # Build list of pid files
    if file == None:
        file_list = glob.glob(directory + appliance + '.pid')
    else:
        file_list = []

        try:
            with open(file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')

                for exporter in csv_reader:
                    if appliance != None and not fnmatch.fnmatch(exporter[0], appliance):
                        continue

                    file_list.append(directory + exporter[0] + '.pid')
        except FileNotFoundError as err:
            print(str(err))
            sys.exit(1)

    return file_list

def get_version():

    return 'v0.3'

def resolve_directory(args):
    """Resolve the directory to use"""

    directory = args.directory
    if os.getenv('MQA_EXPORTER_DIRECTORY') is not None:
        directory = os.getenv('MQA_EXPORTER_DIRECTORY')
    if directory != '':
        directory = directory.replace('\\', '/')
        if not directory.endswith('/'):
            directory += '/'

    return directory
