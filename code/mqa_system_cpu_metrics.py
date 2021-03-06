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

"""This module implements the MQ Appliance system CPU metrics collector"""

import json
import time

from mqalib import call_rest_api
from prometheus_client.core import GaugeMetricFamily

class MQASystemCpuMetrics(object):
    """MQ Appliance system CPU metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):

        start = time.time()

        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/SystemCpuStatus', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        g = GaugeMetricFamily('mqa_system_cpu_usage', 'The instantaneous CPU usage as a percentage of the CPU load', labels=['appliance'])
        g.add_metric([self.appliance], data['SystemCpuStatus']['CpuUsage'])
        yield g

        g = GaugeMetricFamily('mqa_system_cpu_load_avg_1m', 'The average CPU load over the last minute', labels=['appliance'])
        g.add_metric([self.appliance], data['SystemCpuStatus']['CpuLoadAvg1'])
        yield g

        g = GaugeMetricFamily('mqa_system_cpu_load_avg_5m', 'The average CPU load over 5 minutes', labels=['appliance'])
        g.add_metric([self.appliance], data['SystemCpuStatus']['CpuLoadAvg5'])
        yield g

        g = GaugeMetricFamily('mqa_system_cpu_load_avg_15m', 'The average CPU load over 15 minutes', labels=['appliance'])
        g.add_metric([self.appliance], data['SystemCpuStatus']['CpuLoadAvg15'])
        yield g

        g = GaugeMetricFamily('mqa_exporter_system_cpu_elapsed_time_seconds', 'Exporter eleapsed time to collect system cpu metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.time() - start)
        yield g