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

"""This module implements the MQ Appliance raid battery module metrics collector"""

import json
import time

from mqalib import call_rest_api
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily

class MQARaidBatteryModuleMetrics(object):
    """MQ Appliance raid battery module metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):

        start = time.time()

        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/RaidBatteryModuleStatus', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        g = GaugeMetricFamily('mqa_raid_battery_module_voltage_volts', 'The actual voltage of the battery in volts', labels=['appliance', 'controllerID', 'status'])
        g.add_metric([self.appliance, str(data['RaidBatteryModuleStatus']['ControllerID']), str(data['RaidBatteryModuleStatus']['Status'])], data['RaidBatteryModuleStatus']['Voltage'] / 1000)
        yield g

        g = GaugeMetricFamily('mqa_raid_battery_module_current_amperes', 'The current that flows through the battery terminals in amperes', labels=['appliance', 'controllerID', 'status'])
        g.add_metric([self.appliance, str(data['RaidBatteryModuleStatus']['ControllerID']), str(data['RaidBatteryModuleStatus']['Status'])], data['RaidBatteryModuleStatus']['Current'] / 1000)
        yield g

        g = GaugeMetricFamily('mqa_raid_battery_module_temperature_celsius', 'The temperature of the battery in degrees celsius', labels=['appliance', 'controllerID', 'status'])
        g.add_metric([self.appliance, str(data['RaidBatteryModuleStatus']['ControllerID']), str(data['RaidBatteryModuleStatus']['Status'])], data['RaidBatteryModuleStatus']['Temperature'])
        yield g

        g = GaugeMetricFamily('mqa_raid_battery_module_design_capacity_amperes_hour', 'The designed capacity of the battery in ampere-hour', labels=['appliance', 'controllerID', 'status'])
        g.add_metric([self.appliance, str(data['RaidBatteryModuleStatus']['ControllerID']), str(data['RaidBatteryModuleStatus']['Status'])], data['RaidBatteryModuleStatus']['DesignCapacity'] / 1000)
        yield g

        g = GaugeMetricFamily('mqa_raid_battery_module_design_voltage_volts', 'The designed voltage of the battery in volts', labels=['appliance', 'controllerID', 'status'])
        g.add_metric([self.appliance, str(data['RaidBatteryModuleStatus']['ControllerID']), str(data['RaidBatteryModuleStatus']['Status'])], data['RaidBatteryModuleStatus']['DesignVoltage'] / 1000)
        yield g

        i = InfoMetricFamily('mqa_raid_battery_module', 'MQ Appliance raid battery module information')
        i.add_metric(['appliance', 'controllerID', 'batteryType', 'serial', 'name', 'status', 'voltage', 'current',
                          'temperature', 'designCapacity', 'designVoltage'], 
                      {'appliance': self.appliance, 
                      'controllerID': str(data['RaidBatteryModuleStatus']['ControllerID']),
                      'batteryType': data['RaidBatteryModuleStatus']['BatteryType'],
                      'serial': data['RaidBatteryModuleStatus']['Serial'], 
                      'name': data['RaidBatteryModuleStatus']['Name'], 
                      'status': data['RaidBatteryModuleStatus']['Status'], 
                      'voltage': str(data['RaidBatteryModuleStatus']['Voltage']), 
                      'current': str(data['RaidBatteryModuleStatus']['Current']), 
                      'temperature': str(data['RaidBatteryModuleStatus']['Temperature']), 
                      'designCapacity': str(data['RaidBatteryModuleStatus']['DesignCapacity']), 
                      'designVoltage': str(data['RaidBatteryModuleStatus']['DesignVoltage'])})

        g = GaugeMetricFamily('mqa_exporter_raid_battery_module_elapsed_time_seconds', 'Exporter eleapsed time to collect raid battery module metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.time() - start)
        yield g