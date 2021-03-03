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

"""This module implements the MQ Appliance information metrics collector"""

import json

from mqalib import call_rest_api
from prometheus_client.core import InfoMetricFamily

class MQAInformationMetrics(object):
    """MQ Appliance information metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):
        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/DateTimeStatus', self.ip, self.port, self.session, self.timeout)
        data2 = call_rest_api('/mgmt/status/default/FirmwareStatus', self.ip, self.port, self.session, self.timeout)
        data3 = call_rest_api('/mgmt/status/default/FirmwareVersion3', self.ip, self.port, self.session, self.timeout)

        if data == '' or data2 == '' or data3 == '':
            return

        # Update Prometheus metrics
        i = InfoMetricFamily('mqa', 'MQ Appliance information')
        i.add_metric(['appliance', 'time', 'timezone', 'tzspec', 'uptime', 'bootuptime', 'type', 'installdate', 'bootcount', 'serial', 'version', 'level',
                      'build', 'builddate', 'deliverytype', 'watchdogbuild', 'installeddpos', 'runningdpos', 'xmlaccelerator', 'machinetype', 'modeltype'], 
                      {'appliance': self.appliance, 'time': data['DateTimeStatus']['time'], 'timezone': data['DateTimeStatus']['timezone'],
                      'tzspec': data['DateTimeStatus']['tzspec'], 'uptime': data['DateTimeStatus']['uptime2'], 'bootuptime': data['DateTimeStatus']['bootuptime2'],
                      'type': data2['FirmwareStatus']['Type'], 'installdate': data2['FirmwareStatus']['InstallDate'], 'bootcount': str(data2['FirmwareStatus']['BootCount']),
                     'serial': data3['FirmwareVersion3']['Serial'], 'version': data3['FirmwareVersion3']['Version'], 'level': data3['FirmwareVersion3']['Level'],
                     'build': data3['FirmwareVersion3']['Build'], 'builddate': data3['FirmwareVersion3']['BuildDate'], 'deliverytype': data3['FirmwareVersion3']['DeliveryType'],
                     'watchdogbuild': data3['FirmwareVersion3']['WatchdogBuild'], 'installeddpos': data3['FirmwareVersion3']['InstalledDPOS'],
                     'runningdpos': data3['FirmwareVersion3']['RunningDPOS'], 'xmlaccelerator': data3['FirmwareVersion3']['XMLAccelerator'],
                     'machinetype': data3['FirmwareVersion3']['MachineType'], 'modeltype': data3['FirmwareVersion3']['ModelType']})
        yield i
