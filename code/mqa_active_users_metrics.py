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

"""This module implements the MQ Appliance active users metrics collector"""

import requests
import json

from datetime import datetime
from mqalib import call_rest_api
from prometheus_client.core import GaugeMetricFamily

class MQAActiveUsersMetrics(object):
    """MQ Appliance active users metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):
        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/ActiveUsers', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        connections = {}
        users = []

        if type(data['ActiveUsers']) is dict:
            users.append(data['ActiveUsers'])
        else:
            users = data['ActiveUsers']

        # Process active users
        for au in users:

            conn = au['connection']
            if conn in connections:
                count = connections.get(conn)
                count += 1
                connections.update({conn:count})
            else:
                connections.update({conn:1})

        # Update Prometheus metrics
        for conn in connections:
            
            g = GaugeMetricFamily('mqa_active_users_total', 'Total active users connected to the appliance', labels=['appliance', 'connection'])
            g.add_metric([self.appliance, conn], connections.get(conn))
            yield g
