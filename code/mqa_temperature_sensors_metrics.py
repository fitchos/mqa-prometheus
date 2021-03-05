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

"""This module implements the MQ Appliance temperature sensors metrics collector"""

import json

from mqalib import call_rest_api
from prometheus_client.core import GaugeMetricFamily

class MQATemperatureSensorsMetrics(object):
    """MQ Appliance temperature sensors metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):
        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/TemperatureSensors', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        for ts in data['TemperatureSensors']:

            if ts['Name'] == 'CPU DIMM 1 Channel A Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_a_temperature_celsius', 'CPU DIMM 1 channel A temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_a_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU DIMM 1 channel A in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_a_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU DIMM 1 channel A in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_a_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU DIMM 1 channel A in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'CPU DIMM 1 Channel B Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_b_temperature_celsius', 'CPU DIMM 1 channel B temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_b_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU DIMM 1 channel B in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_b_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU DIMM 1 channel B in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_b_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU DIMM 1 channel B in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'CPU DIMM 1 Channel C Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_c_temperature_celsius', 'CPU DIMM 1 channel C temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_c_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU DIMM 1 channel C in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_c_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU DIMM 1 channel C in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_c_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU DIMM 1 channel C in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'CPU DIMM 1 Channel D Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_d_temperature_celsius', 'CPU DIMM 1 channel D temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_d_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU DIMM 1 channel D in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_d_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU DIMM 1 channel D in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_d_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU DIMM 1 channel D in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'CPU DIMM 1 Channel E Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_e_temperature_celsius', 'CPU DIMM 1 channel E temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_e_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU DIMM 1 channel E in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_e_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU DIMM 1 channel E in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_e_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU DIMM 1 channel E in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'CPU DIMM 1 Channel F Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_f_temperature_celsius', 'CPU DIMM 1 channel F temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_f_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU DIMM 1 channel F in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_f_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU DIMM 1 channel F in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_f_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU DIMM 1 channel F in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'CPU DIMM 1 Channel G Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_g_temperature_celsius', 'CPU DIMM 1 channel G temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_g_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU DIMM 1 channel G in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_g_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU DIMM 1 channel G in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_g_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU DIMM 1 channel G in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'CPU DIMM 1 Channel H Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_h_temperature_celsius', 'CPU DIMM 1 channel H temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_h_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU DIMM 1 channel H in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_h_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU DIMM 1 channel H in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_h_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU DIMM 1 channel H in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'CPU DIMM 1 Channel J Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_j_temperature_celsius', 'CPU DIMM 1 channel J temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_j_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU DIMM 1 channel J in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_j_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU DIMM 1 channel J in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_j_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU DIMM 1 channel J in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'CPU DIMM 1 Channel K Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_k_temperature_celsius', 'CPU DIMM 1 channel K temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_k_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU DIMM 1 channel K in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_k_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU DIMM 1 channel K in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_k_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU DIMM 1 channel K in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'CPU DIMM 1 Channel L Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_l_temperature_celsius', 'CPU DIMM 1 channel L temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_l_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU DIMM 1 channel L in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_l_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU DIMM 1 channel L in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_l_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU DIMM 1 channel L in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'CPU DIMM 1 Channel M Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_m_temperature_celsius', 'CPU DIMM 1 channel M temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_m_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU DIMM 1 channel M in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_m_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU DIMM 1 channel M in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_dimm_1_channel_m_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU DIMM 1 channel M in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'Hardware Monitors Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_hardware_monitors_temperature_celsius', 'Hardware monitors temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_hardware_monitors_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for hardware monitors in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_hardware_monitors_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for hardware monitors in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_hardware_monitors_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for hardware monitors in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'PCH Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_pch_temperature_celsius', 'PCH temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_pch_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for PCH in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_pch_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for PCH in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_pch_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for PCH in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'Power Supply 1 Hotspot Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_1_hotspot_temperature_celsius', 'Power supply 1 hotspot temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_1_hotspot_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for power supply 1 hotspot in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_1_hotspot_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for power supply 1 hotspot in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_1_hotspot_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for power supply 1 hotspot in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'Power Supply 2 Hotspot Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_2_hotspot_temperature_celsius', 'Power supply 2 hotspot temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_2_hotspot_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for power supply 2 hotspot in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_2_hotspot_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for power supply 2 hotspot in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_2_hotspot_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for power supply 2 hotspot in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'Power Supply 1 Intake Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_1_intake_temperature_celsius', 'Power supply 1 intake temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_1_intake_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for power supply 1 intake in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_1_intake_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for power supply 1 intake in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_1_intake_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for power supply 1 intake in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'Power Supply 2 Intake Temperature':
                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_2_intake_temperature_celsius', 'Power supply 2 intake temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_2_intake_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for power supply 2 intake in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_2_intake_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for power supply 2 intake in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_power_supply_2_intake_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for power supply 2 intake in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'Temperature CPU1':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_1_temperature_celsius', 'CPU 1 temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu__upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU 1 in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_1_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU 1 in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_1_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU 1 in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'Temperature CPU2':
                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_2_temperature_celsius', 'CPU 2 temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_2_upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for CPU 2 in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_2_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for CPU 2 in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_cpu_2_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for CPU 2 in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'Temperature Inlet 1':
                g = GaugeMetricFamily('mqa_temperature_sensor_inlet_1_temperature_celsius', 'Inlet 1 temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_inlet__upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for inlet 1 in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_inlet_1_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for inlet 1 in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_inlet_1_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for inlet 1 in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g

                continue

            if ts['Name'] == 'Temperature Outlet 1':
                g = GaugeMetricFamily('mqa_temperature_sensor_outlet_1_temperature_celsius', 'Outlet 1 temperature in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['Value'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_outlet__upper_non_critical_threshold_temperature_celsius', 'Upper non critical temperature threshold for outlet 1 in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperNonCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_outlet_1_upper_critical_threshold_temperature_celsius', 'Upper critical temperature threshold for outlet 1 in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], ts['UpperCriticalThreshold'])
                yield g

                g = GaugeMetricFamily('mqa_temperature_sensor_outlet_1_upper_non_recoverable_threshold_temperature_celsius', 'Upper non recoverable temperature threshold for outlet 1 in celsius', labels=['appliance', 'readingStatus'])
                g.add_metric([self.appliance, ts['ReadingStatus']], -1 if ts['UpperNonRecoverableThreshold'] == '' else ts['UpperNonRecoverableThreshold'])
                yield g







