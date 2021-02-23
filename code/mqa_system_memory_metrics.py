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

"""This module implements the MQ Appliance system memory metrics collector"""

import requests
import json

from datetime import datetime
from mqalib import call_rest_api
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily

class MQASystemMemoryMetrics(object):
    """MQ Appliance system memory metrics collector"""

    def __init__(self, appliance, ip, port, auth, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.auth = auth
        self.timeout = timeout

    def collect(self):
        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/SystemMemoryStatus', self.ip, self.port, self.auth, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        g = GaugeMetricFamily('mqa_system_memory_memory_usage', 'The instantaneous memory usage as a percentage of the total memory', labels=['appliance'])
        g.add_metric([self.appliance], data['SystemMemoryStatus']['MemoryUsage'])
        yield g

        c = CounterMetricFamily('mqa_system_memory_memory_bytes_total', 'The total memory of the system in bytes. The total memory equals the amount of installed memory minus the amount of reserved memory', labels=['appliance'])
        c.add_metric([self.appliance], data['SystemMemoryStatus']['TotalMemory']  * 1048576)
        yield c

        g = GaugeMetricFamily('mqa_system_memory_memory_bytes_used', 'The amount of memory in bytes that is currently in use. The used memory equals the amount of total memory minus the amount of free memory. The used memory does not include any hold memory', labels=['appliance'])
        g.add_metric([self.appliance], data['SystemMemoryStatus']['UsedMemory'] * 1048576)
        yield g

        g = GaugeMetricFamily('mqa_system_memory_memory_bytes_free', 'The amount of memory in bytes that is currently not in use and is therefore available. The free memory value includes any hold memory that is not currently in use', labels=['appliance'])
        g.add_metric([self.appliance], data['SystemMemoryStatus']['FreeMemory'] * 1048576)
        yield g