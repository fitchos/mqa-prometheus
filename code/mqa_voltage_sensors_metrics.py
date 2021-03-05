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

"""This module implements the MQ Appliance voltage sensors metrics collector"""

import json
import time

from mqalib import call_rest_api
from prometheus_client.core import GaugeMetricFamily

class MQAVoltageSensorsMetrics(object):
    """MQ Appliance voltage sensors metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):

        start = time.perf_counter()

        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/VoltageSensors', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        for vs in data['VoltageSensors']:

            if vs['Name'] == 'Power Supply 1 In Voltage':
                g = GaugeMetricFamily('mqa_voltage_sensor_power_supply_1_in_voltage_volts', 'Voltage going in power supply 1 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_power_supply_1_in_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of voltage going in power supply 1 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_power_supply_1_in_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of voltage going in power supply 1 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

            if vs['Name'] == 'Power Supply 1 Out Voltage':
                g = GaugeMetricFamily('mqa_voltage_sensor_power_supply_1_out_voltage_volts', 'Voltage going out power supply 1 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_power_supply_1_out_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of voltage going out power supply 1 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_power_supply_1_out_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of voltage going out power supply 1 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

            if vs['Name'] == 'Power Supply 2 In Voltage':
                g = GaugeMetricFamily('mqa_voltage_sensor_power_supply_2_in_voltage_volts', 'Voltage going in power supply 2 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_power_supply_2_in_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of voltage going in power supply 2 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_power_supply_2_in_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of voltage going in power supply 2 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

            if vs['Name'] == 'Power Supply 2 Out Voltage':
                g = GaugeMetricFamily('mqa_voltage_sensor_power_supply_2_out_voltage_volts', 'Voltage going out power supply 2 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_power_supply_2_out_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of voltage going out power supply 2 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_power_supply_2_out_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of voltage going out power supply 2 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

            if vs['Name'] == 'Voltage +1.5':
                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_15_volts', 'Voltage +1.5 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_15_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of +1.5 voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_15_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of +1.5 voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

            if vs['Name'] == 'Voltage +1.8':
                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_18_volts', 'Voltage +1.8 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_18_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of +1.8 voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_18_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of +1.8 voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

            if vs['Name'] == 'Voltage +12':
                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_12_volts', 'Voltage +12 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_12_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of +12 voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_12_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of +12 voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

            if vs['Name'] == 'Voltage +3.3':
                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_33_volts', 'Voltage +3.3 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_33_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of +3.3 voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_33_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of +3.3 voltage +3.3 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

            if vs['Name'] == 'Voltage +5':
                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_5_volts', 'Voltage +5 in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_5_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of +5 voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_5_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of +5 voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

            if vs['Name'] == 'Voltage +5 Standby':
                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_5_standby_volts', 'Voltage +5 standby in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_5_standby_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of +5 standby voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_5_standby_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of +5 standby voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

            if vs['Name'] == 'Voltage Battery':
                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_battery_volts', 'Voltage battery in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_battery_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of battery voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_battery_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of battery voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

            if vs['Name'] == 'Voltage CPU1 Core':
                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_cpu1_core_volts', 'Voltage CPU 1 core in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_cpu1_core_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of CPU 1 core voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_cpu1_core_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of CPU 1 core voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

            if vs['Name'] == 'Voltage CPU2 Core':
                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_cpu2_core_volts', 'Voltage CPU 2 core in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['Value'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_cpu2_core_lower_critical_thereshold_voltage_volts', 'Lower critical threshold of CPU 2 core voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['LowerCriticalThreshold'] / 1000)
                yield g

                g = GaugeMetricFamily('mqa_voltage_sensor_voltage_cpu2_core_upper_critical_thereshold_voltage_volts', 'Upper critical threshold of CPU 2 core voltage in volts', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, vs['ReadingStatus']], vs['UpperCriticalThreshold'] / 1000)
                yield g

                continue

        g = GaugeMetricFamily('mqa_exporter_voltage_sensors_elapsed_time_seconds', 'Exporter eleapsed time to collect voltage sensors metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.perf_counter() - start)
        yield g
