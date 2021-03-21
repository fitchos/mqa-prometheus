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
import time

from mqalib import call_rest_api
from mqalib import datetime_to_epoch
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily, InfoMetricFamily

class MQAInformationMetrics(object):
    """MQ Appliance information metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):

        start = time.time()

        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/DateTimeStatus', self.ip, self.port, self.session, self.timeout)
        data2 = call_rest_api('/mgmt/status/default/FirmwareStatus', self.ip, self.port, self.session, self.timeout)
        data3 = call_rest_api('/mgmt/status/default/FirmwareVersion3', self.ip, self.port, self.session, self.timeout)

        if data == '' or data2 == '' or data3 == '':
            return

        # Update Prometheus metrics
        c = CounterMetricFamily('mqa_bootcount', 'The number of times the firmware image was restarted through an appliance reboot or a firmware reload. The count is from the initial firmware load on the appliance till the current time. The count is independent of firmware version', labels=['appliance'])
        c.add_metric([self.appliance], data2['FirmwareStatus']['BootCount'])
        yield c

        uptime_split = data['DateTimeStatus']['uptime2'].split(' ')
        days = int(uptime_split[0])
        hours = int(uptime_split[2][0:2])
        minutes = int(uptime_split[2][3:5])
        seconds = int(uptime_split[2][6:])
        uptime_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds

        c = CounterMetricFamily('mqa_uptime_seconds', 'The total amount of time in seconds the appliance has been up since the last reload or reboot. Note that a shutdown and reload resets this counter', labels=['appliance'])
        c.add_metric([self.appliance], uptime_seconds)
        yield c

        bootuptime_split = data['DateTimeStatus']['bootuptime2'].split(' ')
        days = int(bootuptime_split[0])
        hours = int(bootuptime_split[2][0:2])
        minutes = int(bootuptime_split[2][3:5])
        seconds = int(bootuptime_split[2][6:])
        bootuptime_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds

        c = CounterMetricFamily('mqa_bootuptime_seconds', 'The total amount of time in seconds since the last reboot. Note that this counter is reset by a shutdown and reboot, but not by a shutdown and reload', labels=['appliance'])
        c.add_metric([self.appliance], bootuptime_seconds)
        yield c

        c = CounterMetricFamily('mqa_current_datetime_seconds', 'The current date and time of the MQ Appliance in epoch seconds', labels=['appliance'])
        c.add_metric([self.appliance], datetime_to_epoch(data['DateTimeStatus']['time'], '%a %b %d %H:%M:%S %Y'))
        yield c

        i = InfoMetricFamily('mqa', 'MQ Appliance information')
        i.add_metric(['appliance', 'timezone', 'tzspec', 'type', 'installdate', 'serial', 'version', 'level',
                      'build', 'builddate', 'deliverytype', 'watchdogbuild', 'installeddpos', 'runningdpos', 'xmlaccelerator', 'machinetype', 'modeltype'], 
                      {'appliance': self.appliance, 'timezone': data['DateTimeStatus']['timezone'],
                      'tzspec': data['DateTimeStatus']['tzspec'], 
                      'type': data2['FirmwareStatus']['Type'], 'installdate': data2['FirmwareStatus']['InstallDate'],
                     'serial': data3['FirmwareVersion3']['Serial'], 'version': data3['FirmwareVersion3']['Version'], 'level': data3['FirmwareVersion3']['Level'],
                     'build': data3['FirmwareVersion3']['Build'], 'builddate': data3['FirmwareVersion3']['BuildDate'], 'deliverytype': data3['FirmwareVersion3']['DeliveryType'],
                     'watchdogbuild': data3['FirmwareVersion3']['WatchdogBuild'], 'installeddpos': data3['FirmwareVersion3']['InstalledDPOS'],
                     'runningdpos': data3['FirmwareVersion3']['RunningDPOS'], 'xmlaccelerator': data3['FirmwareVersion3']['XMLAccelerator'],
                     'machinetype': data3['FirmwareVersion3']['MachineType'], 'modeltype': data3['FirmwareVersion3']['ModelType']})
        yield i

        g = GaugeMetricFamily('mqa_exporter_mqa_information_elapsed_time_seconds', 'Exporter eleapsed time to collect mqa information metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.time() - start)
        yield g
