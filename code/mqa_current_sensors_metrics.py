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

"""This module implements the MQ Appliance current sensors metrics collector"""

import json
import time

from mqalib import call_rest_api
from prometheus_client.core import GaugeMetricFamily

class MQACurrentSensorsMetrics(object):
    """MQ Appliance current sensors metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):

        start = time.time()

        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/CurrentSensors', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        for cs in data['CurrentSensors']:

            if cs['Name'] == 'Power Supply 1 In Current':
                g = GaugeMetricFamily('mqa_current_sensors_power_supply_1_in_current_upper_critical_threshold_amperes', 'Upper critical threshold for current going into power supply 1', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, cs['ReadingStatus']], cs['UpperCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_current_sensors_power_supply_1_in_current_amperes', 'Current going into power supply 1', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, cs['ReadingStatus']], cs['Value'] / 1000)
                yield g

            if cs['Name'] == 'Power Supply 1 Out Current':
                g = GaugeMetricFamily('mqa_current_sensors_power_supply_1_out_current_upper_critical_threshold_amperes', 'Upper critical threshold for current going out power supply 1', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, cs['ReadingStatus']], cs['UpperCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_current_sensors_power_supply_1_out_current_amperes', 'Current going out power supply 1', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, cs['ReadingStatus']], cs['Value'] / 1000)
                yield g

            if cs['Name'] == 'Power Supply 2 In Current':
                g = GaugeMetricFamily('mqa_current_sensors_power_supply_2_in_current_upper_critical_threshold_amperes', 'Upper critical threshold for current going into power supply 2', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, cs['ReadingStatus']], cs['UpperCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_current_sensors_power_supply_2_in_current_amperes', 'Current going into power supply 2', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, cs['ReadingStatus']], cs['Value'] / 1000)
                yield g

            if cs['Name'] == 'Power Supply 2 Out Current':
                g = GaugeMetricFamily('mqa_current_sensors_power_supply_2_out_current_upper_critical_threshold_amperes', 'Upper critical threshold for current going out power supply 2', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, cs['ReadingStatus']], cs['UpperCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_current_sensors_power_supply_2_out_current_amperes', 'Current going out power supply 2', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, cs['ReadingStatus']], cs['Value'] / 1000)
                yield g
        
        g = GaugeMetricFamily('mqa_exporter_current_sensors_elapsed_time_seconds', 'Exporter eleapsed time to collect current sensors metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.time() - start)
        yield g

        