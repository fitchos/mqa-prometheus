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

"""This module implements the MQ Appliance file system metrics collector"""

import json
import time

from mqalib import call_rest_api
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily

class MQAFileSystemMetrics(object):
    """MQ Appliance file system metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):

        start = time.time()

        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/FilesystemStatus', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        g = GaugeMetricFamily('mqa_file_system_encrypted_bytes_free', 'Free, or unused and available, encrypted storage space on the appliance', labels=['appliance'])
        # Memory in MB not MiB 
        #g.add_metric([self.appliance], data['FilesystemStatus']['FreeEncrypted'] * 1048576)
        g.add_metric([self.appliance], data['FilesystemStatus']['FreeEncrypted'] * 1000000)
        yield g

        c = CounterMetricFamily('mqa_file_system_encrypted_bytes_total', 'Total encrypted storage space on the appliance (the maximum capacity)', labels=['appliance'])
        # Memory in MB not MiB 
        #c.add_metric([self.appliance], data['FilesystemStatus']['TotalEncrypted'] * 1048576)
        c.add_metric([self.appliance], data['FilesystemStatus']['TotalEncrypted'] * 1000000)
        yield c

        g = GaugeMetricFamily('mqa_file_system_temporary_bytes_free', 'Free, or unused and available, temporary storage space on the appliance', labels=['appliance'])
        # Memory in MB not MiB 
        #g.add_metric([self.appliance], data['FilesystemStatus']['FreeTemporary'] * 1048576)
        g.add_metric([self.appliance], data['FilesystemStatus']['FreeTemporary'] * 1000000)
        yield g

        c = CounterMetricFamily('mqa_file_system_temporary_bytes_total', 'Total temporary storage space on the appliance', labels=['appliance'])
        # Memory in MB not MiB 
        #c.add_metric([self.appliance], data['FilesystemStatus']['TotalTemporary'] * 1048576)
        c.add_metric([self.appliance], data['FilesystemStatus']['TotalTemporary'] * 1000000)
        yield c

        g = GaugeMetricFamily('mqa_file_system_internal_bytes_free', 'Free, or unused and available, internal storage space on the appliance', labels=['appliance'])
        # Memory in MB not MiB 
        #g.add_metric([self.appliance], data['FilesystemStatus']['FreeInternal'] * 1048576)
        g.add_metric([self.appliance], data['FilesystemStatus']['FreeInternal'] * 1000000)
        yield g

        c = CounterMetricFamily('mqa_file_system_internal_bytes_total', 'Total internal storage space on the appliance', labels=['appliance'])
        # Memory in MB not MiB 
        #c.add_metric([self.appliance], data['FilesystemStatus']['TotalInternal'] * 1048576)
        c.add_metric([self.appliance], data['FilesystemStatus']['TotalInternal'] * 1000000)
        yield c

        g = GaugeMetricFamily('mqa_exporter_file_system_elapsed_time_seconds', 'Exporter eleapsed time to collect file system metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.time() - start)
        yield g