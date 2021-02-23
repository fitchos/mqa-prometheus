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

import json
import logging
import requests

from datetime import datetime

def call_rest_api(api_call, ip, port, auth, timeout):
    """Perform a REST API call"""

    requests.packages.urllib3.disable_warnings()

    logging.info('Performing REST API call to gather \'' + api_call + '\'...')
    try:
        response = requests.get('https://' + ip + ':' + port + api_call, timeout=timeout, verify=False, auth=auth)
        if response.status_code == 200:
            data = json.loads(response.text)

            if 'result' in data:
                logging.error('REST API call to gather \'' + api_call  + '\' failed --> ' + data['result'])
                return ''
        else:
            logging.error('REST API call to gather \'' + api_call  + '\' failed --> HTTP status code is ' + str(response.status_code) + ' (' + response.reason + ')')
            return ''
    except requests.RequestException as err:
        logging.error('REST API call to gather \'' + api_call  + '\' failed --> ' + str(err))
        return ''

    logging.info('REST API call to gather \'' + api_call  + '\' completed.')

    return data
