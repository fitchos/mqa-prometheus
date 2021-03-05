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

"""This module implements the MQ Appliance other sensors metrics collector"""

import json
import time

from mqalib import call_rest_api
from prometheus_client.core import GaugeMetricFamily

class MQAOtherSensorsMetrics(object):
    """MQ Appliance other sensors metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):

        start = time.perf_counter()

        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/OtherSensors', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        for os in data['OtherSensors']:

            if os['Name'] == 'Intrusion Detected':
                g = GaugeMetricFamily('mqa_other_sensor_intrusion_detected', 'Whether an intrusion has been detected', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, os['ReadingStatus']], 1 if os['Value'] == 'true' else 0)
                yield g
                continue

            if os['Name'] == 'Power Supply 1 AC Lost':
                g = GaugeMetricFamily('mqa_other_sensor_power_supply_1_ac_lost', 'Whether power supply 1 lost AC', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, os['ReadingStatus']], 1 if os['Value'] == 'true' else 0)
                yield g
                continue

            if os['Name'] == 'Power Supply 1 Not Enabled':
                g = GaugeMetricFamily('mqa_other_sensor_power_supply_1_not_enabled', 'Whether power supply 1 is not enabled', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, os['ReadingStatus']], 1 if os['Value'] == 'true' else 0)
                yield g
                continue

            if os['Name'] == 'Power Supply 1 Output Failure':
                g = GaugeMetricFamily('mqa_other_sensor_power_supply_1_output_failure', 'Whether power supply 1 has an output failure', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, os['ReadingStatus']], 1 if os['Value'] == 'true' else 0)
                yield g
                continue

            if os['Name'] == 'Power Supply 1 Present':
                g = GaugeMetricFamily('mqa_other_sensor_power_supply_1_present', 'Whether power supply 1 is present', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, os['ReadingStatus']], 1 if os['Value'] == 'true' else 0)
                yield g
                continue

            if os['Name'] == 'Power Supply 2 AC Lost':
                g = GaugeMetricFamily('mqa_other_sensor_power_supply_2_ac_lost', 'Whether power supply 2 lost AC', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, os['ReadingStatus']], 1 if os['Value'] == 'true' else 0)
                yield g
                continue

            if os['Name'] == 'Power Supply 2 Not Enabled':
                g = GaugeMetricFamily('mqa_other_sensor_power_supply_2_not_enabled', 'Whether power supply 2 is not enabled', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, os['ReadingStatus']], 1 if os['Value'] == 'true' else 0)
                yield g
                continue

            if os['Name'] == 'Power Supply 2 Output Failure':
                g = GaugeMetricFamily('mqa_other_sensor_power_supply_2_output_failure', 'Whether power supply 2 has an output failure', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, os['ReadingStatus']], 1 if os['Value'] == 'true' else 0)
                yield g
                continue

            if os['Name'] == 'Power Supply 2 Present':
                g = GaugeMetricFamily('mqa_other_sensor_power_supply_2_present', 'Whether power supply 2 is present', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, os['ReadingStatus']], 1 if os['Value'] == 'true' else 0)
                yield g
                continue

        g = GaugeMetricFamily('mqa_exporter_other_sensors_elapsed_time_seconds', 'Exporter eleapsed time to collect other sensors metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.perf_counter() - start)
        yield g
