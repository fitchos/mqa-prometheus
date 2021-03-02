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

"""This module implements the MQ Appliance environmental sensors metrics collector"""

import requests
import json

from datetime import datetime
from mqalib import call_rest_api
from prometheus_client.core import GaugeMetricFamily

class MQAEnvironmentalSensorsMetrics(object):
    """MQ Appliance environmental sensors metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):
        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/EnvironmentalSensors', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        g = GaugeMetricFamily('mqa_environmental_sensors_system_temperature_celsius', 'Ambient temperature', labels=['appliance'])
        g.add_metric([self.appliance], data['EnvironmentalSensors']['systemTemp'])
        yield g

        g = GaugeMetricFamily('mqa_environmental_sensors_cpu_1_temperature_celsius', 'CPU 1 temperature', labels=['appliance'])
        g.add_metric([self.appliance], data['EnvironmentalSensors']['cpu1Temp'])
        yield g

        g = GaugeMetricFamily('mqa_environmental_sensors_cpu_2_temperature_celsius', 'CPU 2 temperature', labels=['appliance'])
        g.add_metric([self.appliance], data['EnvironmentalSensors']['cpu2Temp'])
        yield g

        g = GaugeMetricFamily('mqa_environmental_sensors_cpu_1_fan_speed_rpm', 'CPU 1 fan speed', labels=['appliance'])
        g.add_metric([self.appliance], data['EnvironmentalSensors']['cpu1rpm'])
        yield g

        g = GaugeMetricFamily('mqa_environmental_sensors_cpu_2_fan_speed_rpm', 'CPU 2 fan speed', labels=['appliance'])
        g.add_metric([self.appliance], data['EnvironmentalSensors']['cpu2rpm'])
        yield g

        g = GaugeMetricFamily('mqa_environmental_sensors_chassis_fan_1_speed_rpm', 'Chassis fan 1 speed', labels=['appliance'])
        g.add_metric([self.appliance], data['EnvironmentalSensors']['chassis1rpm'])
        yield g

        g = GaugeMetricFamily('mqa_environmental_sensors_chassis_fan_2_speed_rpm', 'Chassis fan 2 speed', labels=['appliance'])
        g.add_metric([self.appliance], data['EnvironmentalSensors']['chassis2rpm'])
        yield g

        g = GaugeMetricFamily('mqa_environmental_sensors_chassis_fan_3_speed_rpm', 'Chassis fan 3 speed', labels=['appliance'])
        g.add_metric([self.appliance], data['EnvironmentalSensors']['chassis3rpm'])
        yield g

        g = GaugeMetricFamily('mqa_environmental_sensors_33_voltage', '3.3 voltage', labels=['appliance'])
        g.add_metric([self.appliance], float(data['EnvironmentalSensors']['volt33']))
        yield g

        g = GaugeMetricFamily('mqa_environmental_sensors_5_voltage', '5 voltage', labels=['appliance'])
        g.add_metric([self.appliance], float(data['EnvironmentalSensors']['volt5']))
        yield g

        g = GaugeMetricFamily('mqa_environmental_sensors_12_voltage', '12 voltage', labels=['appliance'])
        g.add_metric([self.appliance], float(data['EnvironmentalSensors']['volt12']))
        yield g