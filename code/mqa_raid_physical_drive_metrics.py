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

"""This module implements the MQ Appliance raid physical drive metrics collector"""

import json
import time

from mqalib import call_rest_api
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily, InfoMetricFamily

class MQARaidPhysicalDriveMetrics(object):
    """MQ Appliance raid physical drive metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):

        start = time.time()

        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/RaidPhysicalDriveStatus', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        for rpd in data['RaidPhysicalDriveStatus']:

            c = CounterMetricFamily('mqa_raid_physical_drive_progress_percent_total', 'The current progress percentage of the operation on the physical drive. Operations can be rebuild, copyback, patrol, or clear.', labels=['appliance', 'controllerID', 'deviceID', 'arrayID', 'logicalDriveID'])
            c.add_metric([self.appliance, str(rpd['ControllerID']), str(rpd['DeviceID']), str(rpd['ArrayID']), str(rpd['LogicalDriveID'])], rpd['ProgressPercent'])
            yield c

            c = CounterMetricFamily('mqa_raid_physical_drive_raw_size_bytes_total', 'The exact size of the drive in bytes', labels=['appliance', 'controllerID', 'deviceID', 'arrayID', 'logicalDriveID'])
            c.add_metric([self.appliance, str(rpd['ControllerID']), str(rpd['DeviceID']), str(rpd['ArrayID']), str(rpd['LogicalDriveID'])], rpd['RawSize'])
            yield c

            c = CounterMetricFamily('mqa_raid_physical_drive_coerced_size_bytes_total', 'The normalized size in megabytes. The value is rounded down to an even multiple, which allows you to swap drives of the same nominal size but might not be the same raw size.', labels=['appliance', 'controllerID', 'deviceID', 'arrayID', 'logicalDriveID'])
            c.add_metric([self.appliance, str(rpd['ControllerID']), str(rpd['DeviceID']), str(rpd['ArrayID']), str(rpd['LogicalDriveID'])], rpd['CoercedSize'])
            yield c

            temperature_celsius = int(rpd['Temperature'][:3])
            g = GaugeMetricFamily('mqa_raid_physical_drive_temperature_celsius', 'The temperature of the hard disk drive in celsius.', labels=['appliance', 'controllerID', 'deviceID', 'arrayID', 'logicalDriveID'])
            g.add_metric([self.appliance, str(rpd['ControllerID']), str(rpd['DeviceID']), str(rpd['ArrayID']), str(rpd['LogicalDriveID'])], temperature_celsius)
            yield g

            i = InfoMetricFamily('mqa_raid_physical_drive', 'MQ Appliance raid physical drive information')
            i.add_metric(['appliance', 'controllerID', 'deviceID', 'arrayID', 'logicalDriveID', 'logicalDriveName', 'position', 'state',
                          'progressPercent', 'rawSize', 'coercedSize', 'interfaceType', 'interfaceSpeed', 'sasAddress', 'vendorID', 'productID',
                          'revision', 'specificInfo', 'failure', 'Temperature'], 
                      {'appliance': self.appliance, 
                      'controllerID': str(rpd['ControllerID']),
                      'deviceID': str(rpd['DeviceID']),
                      'arrayID': str(rpd['ArrayID']), 
                      'logicalDriveID': str(rpd['LogicalDriveID']), 
                      'logicalDriveName': rpd['LogicalDriveName'], 
                      'position': rpd['Position'], 
                      'state': rpd['State'],
                      'progressPercent': str(rpd['ProgressPercent']), 
                      'rawSize': str(rpd['RawSize']), 
                      'coercedSize': str(rpd['CoercedSize']), 
                      'interfaceType': rpd['InterfaceType'],
                      'interfaceSpeed': rpd['InterfaceSpeed'], 
                      'sasAddress': rpd['SASaddress'], 
                      'vendorID': rpd['VendorID'], 
                      'revision': rpd['Revision'],
                      'specificInfo': rpd['SpecificInfo'], 
                      'failure': rpd['Failure'], 
                      'Temperature': rpd['Temperature']})
            yield i

        g = GaugeMetricFamily('mqa_exporter_raid_physical_drive_elapsed_time_seconds', 'Exporter eleapsed time to collect raid physical drive metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.time() - start)
        yield g
             