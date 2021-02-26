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

"""This module implements the MQ Appliance log targets metrics collector"""

import requests
import json

from datetime import datetime
from mqalib import call_rest_api
from prometheus_client.core import CounterMetricFamily, InfoMetricFamily

class MQALogTargetsMetrics(object):
    """MQ Appliance log targets metrics collector"""

    def __init__(self, appliance, ip, port, auth, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.auth = auth
        self.timeout = timeout

    def collect(self):
        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/LogTargetStatus', self.ip, self.port, self.auth, self.timeout)
        if data == '':
            return

        logTargets = []

        if type(data['LogTargetStatus']) is dict:
            logTargets.append(data['LogTargetStatus'])
        else:
            logTargets = data['LogTargetStatus']

        # Update Prometheus metrics
        for lt in logTargets:

            c = CounterMetricFamily('mqa_log_target_events_processed_total', 'The number of events that this log target processed', labels=['appliance', 'name'])
            c.add_metric([self.appliance, lt['LogTarget']['value']], lt['EventsProcessed'])
            yield c

            c = CounterMetricFamily('mqa_log_target_events_dropped_total', 'The number of events that this log target dropped because there are too many pending events', labels=['appliance', 'name'])
            c.add_metric([self.appliance, lt['LogTarget']['value']], lt['EventsDropped'])
            yield c

            c = CounterMetricFamily('mqa_log_target_events_pending_total', 'The number of pending events for this log target. These events are waiting to be stored at the destination', labels=['appliance', 'name'])
            c.add_metric([self.appliance, lt['LogTarget']['value']], lt['EventsPending'])
            yield c

            i = InfoMetricFamily('mqa_log_target', 'MQ Appliance log target information')
            i.add_metric(['appliance', 'name', 'href', 'status', 'errorInfo', 'requestedMemory'], 
                      {'appliance': self.appliance, 
                      'name': lt['LogTarget']['value'],
                      'href': lt['LogTarget']['href'],
                      'status': lt['Status'], 
                      'errorInfo': lt['ErrorInfo'], 
                      'requestedMemory': str(lt['RequestedMemory'])})
            yield i
             