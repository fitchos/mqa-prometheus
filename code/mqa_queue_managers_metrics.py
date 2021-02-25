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

"""This module implements the MQ Appliance queue managers metrics collector"""

import requests
import json

from datetime import datetime
from mqalib import call_rest_api
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily

class MQAQueueManagersMetrics(object):
    """MQ Appliance queue managers metrics collector"""

    def __init__(self, appliance, ip, port, auth, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.auth = auth
        self.timeout = timeout

    def collect(self):
        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/QueueManagersStatus', self.ip, self.port, self.auth, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        for qm in data['QueueManagersStatus']:

            g = GaugeMetricFamily('mqa_queue_manager_cpu_usage', 'The instantaneous CPU usage by the queue manager as a percentage of the CPU load', labels=['appliance', 'qm'])
            g.add_metric([self.appliance, qm['Name']], qm['CpuUsage'])
            yield g

            g = GaugeMetricFamily('mqa_queue_manager_memory_bytes_used', 'The amount of memory in bytes that is currently in use by the queue manager', labels=['appliance', 'qm'])
            g.add_metric([self.appliance, qm['Name']], qm['UsedMemory'] * 1048576)
            yield g

            g = GaugeMetricFamily('mqa_queue_manager_fs_bytes_used', 'The amount of file system in bytes that is currently in use by the queue manager', labels=['appliance', 'qm'])
            g.add_metric([self.appliance, qm['Name']], qm['UsedFs'] * 1048576)
            yield g

            g = GaugeMetricFamily('mqa_queue_manager_fs_bytes_allocated', 'The amount of file system in bytes allocated for the queue manager', labels=['appliance', 'qm'])
            g.add_metric([self.appliance, qm['Name']], qm['TotalFs'] * 1048576)
            yield g

            i = InfoMetricFamily('mqa_queue_manager', 'MQ Appliance queue manager information')
            i.add_metric(['appliance', 'qm', 'status', 'haRole', 'haStatus', 'drRole', 'drStatus'], 
                          {'appliance': self.appliance, 
                          'qm': qm['Name'], 
                          'status': qm['Status'],
                          'haRole': 'Unknown' if qm['HaRole'] == '' else qm['HaRole'],
                          'haStatus': 'Unknown' if qm['HaStatus'] == '' else qm['HaStatus'],
                          'drRole': 'Unknown' if qm['DrRole'] == '' else qm['DrRole'], 
                          'drStatus': 'Unknown' if qm['DrStatus'] == '' else qm['DrStatus']})
            yield i
