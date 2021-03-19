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

"""This module implements the MQ Appliance MQ system resources metrics collector"""

import json
import time

from mqalib import call_rest_api
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily

class MQAMQSystemResourcesMetrics(object):
    """MQ Appliance MQ system resources metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):

        start = time.time()

        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/MQSystemResources', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        c = CounterMetricFamily('mqa_mq_resources_storage_bytes_total', 'The total storage in bytes available for IBM MQ data', labels=['appliance'])
        c.add_metric([self.appliance], data['MQSystemResources']['TotalStorage'] * 1000000)
        yield c

        g = GaugeMetricFamily('mqa_mq_resources_storage_bytes_used', 'The amount of IBM MQ storage in use in bytes', labels=['appliance'])
        g.add_metric([self.appliance], data['MQSystemResources']['UsedStorage'] * 1000000)
        yield g

        c = CounterMetricFamily('mqa_mq_resources_errors_storage_bytes_total', 'The total storage in bytes available for IBM MQ error logs', labels=['appliance'])
        c.add_metric([self.appliance], data['MQSystemResources']['TotalErrorsStorage'] * 1000000)
        yield c

        g = GaugeMetricFamily('mqa_mq_resources_errors_storage_bytes_used', 'The amount of IBM MQ error log storage in use in bytes', labels=['appliance'])
        g.add_metric([self.appliance], data['MQSystemResources']['UsedErrorsStorage'] * 1000000)
        yield g

        c = CounterMetricFamily('mqa_mq_resources_trace_storage_bytes_total', 'The total storage in bytes available for IBM MQ trace', labels=['appliance'])
        c.add_metric([self.appliance], data['MQSystemResources']['TotalTraceStorage'] * 1000000)
        yield c

        g = GaugeMetricFamily('mqa_mq_resources_trace_storage_bytes_used', 'The amount of IBM MQ trace storage in bytes in use', labels=['appliance'])
        g.add_metric([self.appliance], data['MQSystemResources']['UsedTraceStorage'] * 1000000)
        yield g

        g = GaugeMetricFamily('mqa_exporter_mq_system_resources_elapsed_time_seconds', 'Exporter eleapsed time to collect mq system resources metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.time() - start)
        yield g