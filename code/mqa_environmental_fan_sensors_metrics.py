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

"""This module implements the MQ Appliance environmental fan sensors metrics collector"""

import requests
import json

from datetime import datetime
from mqalib import call_rest_api
from prometheus_client.core import GaugeMetricFamily

class MQAEnvironmentalFanSensorsMetrics(object):
    """MQ Appliance environmental fan sensors metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):
        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/EnvironmentalFanSensors', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        for efs in data['EnvironmentalFanSensors']:

            g = GaugeMetricFamily('mqa_environmental_fan_sensors_fan_speed_rpm', 'The speed of the fan in revolutions per minute (RPM)', labels=['appliance', 'fanID', 'readingStatus'])
            g.add_metric([self.appliance, efs['FanID'], efs['ReadingStatus']], efs['FanSpeed'])
            yield g

            g = GaugeMetricFamily('mqa_environmental_fan_sensors_fan_speed_lower_critical_threshold_rpm', 'The lowest allowable reading of the fan speed sensor', labels=['appliance', 'fanId', 'readingStatus'])
            g.add_metric([self.appliance, efs['FanID'], efs['ReadingStatus']], efs['LowerCriticalThreshold'])
            yield g
