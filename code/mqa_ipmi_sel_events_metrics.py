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

"""This module implements the MQ Appliance IPMI SEL events metrics collector"""

import requests
import json

from datetime import datetime
from mqalib import call_rest_api
from prometheus_client.core import InfoMetricFamily

class MQAIPMISelEventsMetrics(object):
    """MQ Appliance IPMI SEL events metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):
        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/IPMISelEvents', self.ip, self.port, self.session, self.timeout)

        if data == '':
            return

        # Update Prometheus metrics
        for ise in data['IPMISelEvents']:
            i = InfoMetricFamily('mqa_ipmi_sel_events', 'MQ Appliance IPMI SEL events information')
            i.add_metric(['appliance', 'index', 'timestamp', 'recordType', 'sensorType', 'sensorNumber', 'sensorName', 'eventReadingTypeCode', 'eventData', 'eventDirection', 'extra'], 
                      {'appliance': self.appliance, 'index': ise['Index'], 'timestamp': ise['Timestamp'],
                      'recordType': ise['RecordType'], 'sensorType': ise['SensorType'], 'sensorNumber': ise['SensorNumber'],
                      'sensorName': ise['SensorName'], 'eventReadingTypeCode': ise['EventReadingTypeCode'], 'eventData': ise['EventData2'],
                      'eventDirection': ise['EventDirection'], 'extra': ise['Extra']})
            yield i
