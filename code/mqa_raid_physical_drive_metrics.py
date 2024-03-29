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

            c = CounterMetricFamily('mqa_raid_physical_drive_progress_percent_total', 'The current progress percentage of the operation on the physical drive. Operations can be rebuild, copyback, patrol, or clear', labels=['appliance', 'controllerID', 'deviceID', 'arrayID', 'logicalDriveID', 'position'])
            c.add_metric([self.appliance, str(rpd['ControllerID']), str(rpd['DeviceID']), str(rpd['ArrayID']), str(rpd['LogicalDriveID']), rpd['Position']], rpd['ProgressPercent'])
            yield c

            c = CounterMetricFamily('mqa_raid_physical_drive_raw_size_bytes_total', 'The exact size of the drive in bytes', labels=['appliance', 'controllerID', 'deviceID', 'arrayID', 'logicalDriveID', 'position'])
            c.add_metric([self.appliance, str(rpd['ControllerID']), str(rpd['DeviceID']), str(rpd['ArrayID']), str(rpd['LogicalDriveID']), rpd['Position']], rpd['RawSize'] * 1000000)
            yield c

            c = CounterMetricFamily('mqa_raid_physical_drive_coerced_size_bytes_total', 'The normalized size in megabytes. The value is rounded down to an even multiple, which allows you to swap drives of the same nominal size but might not be the same raw size', labels=['appliance', 'controllerID', 'deviceID', 'arrayID', 'logicalDriveID', 'position'])
            c.add_metric([self.appliance, str(rpd['ControllerID']), str(rpd['DeviceID']), str(rpd['ArrayID']), str(rpd['LogicalDriveID']), rpd['Position']], rpd['CoercedSize'] * 1000000)
            yield c

            if rpd['Temperature'][:3] == 'n/a':
                temperature_celsius = -1
            else:
                temperature_celsius = int(rpd['Temperature'][:3])
            g = GaugeMetricFamily('mqa_raid_physical_drive_temperature_celsius', 'The temperature of the hard disk drive in celsius', labels=['appliance', 'controllerID', 'deviceID', 'arrayID', 'logicalDriveID', 'position'])
            g.add_metric([self.appliance, str(rpd['ControllerID']), str(rpd['DeviceID']), str(rpd['ArrayID']), str(rpd['LogicalDriveID']), rpd['Position']], temperature_celsius)
            yield g

            g = GaugeMetricFamily('mqa_raid_physical_drive_failure', 'If the hard disk failure state shows Yes, replace this drive as soon as possible to avoid possible data loss', labels=['appliance', 'controllerID', 'deviceID', 'arrayID', 'logicalDriveID', 'position'])
            g.add_metric([self.appliance, str(rpd['ControllerID']), str(rpd['DeviceID']), str(rpd['ArrayID']), str(rpd['LogicalDriveID']), rpd['Position']], 0 if rpd['Failure'] == 'No' else 1)
            yield g

            i = InfoMetricFamily('mqa_raid_physical_drive', 'MQ Appliance raid physical drive information')
            i.add_metric(['appliance', 'controllerID', 'deviceID', 'arrayID', 'logicalDriveID', 'logicalDriveName', 'position', 'state',
                         'interfaceType', 'interfaceSpeed', 'sasAddress', 'vendorID', 'productID',
                        'revision', 'specificInfo', 'failure'], 
                      {'appliance': self.appliance, 
                      'controllerID': str(rpd['ControllerID']),
                      'deviceID': str(rpd['DeviceID']),
                      'arrayID': str(rpd['ArrayID']), 
                      'logicalDriveID': str(rpd['LogicalDriveID']), 
                      'logicalDriveName': rpd['LogicalDriveName'], 
                      'position': rpd['Position'], 
                      'state': rpd['State'],
                      'interfaceType': rpd['InterfaceType'],
                      'interfaceSpeed': rpd['InterfaceSpeed'], 
                      'sasAddress': rpd['SASaddress'], 
                      'vendorID': rpd['VendorID'],
                      'productID': rpd['ProductID'], 
                      'revision': rpd['Revision'],
                      'specificInfo': rpd['SpecificInfo']})
            yield i

        g = GaugeMetricFamily('mqa_exporter_raid_physical_drive_elapsed_time_seconds', 'Exporter eleapsed time to collect raid physical drive metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.time() - start)
        yield g
             