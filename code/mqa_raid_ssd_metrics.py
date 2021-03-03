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

"""This module implements the MQ Appliance raid ssd metrics collector"""

import json

from mqalib import call_rest_api
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily

class MQARaidSsdMetrics(object):
    """MQ Appliance raid ssd metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):
        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/RaidSsdStatus', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        for rss in data['RaidSsdStatus']:

            g = CounterMetricFamily('mqa_raid_ssd_bytes_written_total', 'The total data in bytes written to the drive since manufacture', labels=['appliance', 'diskNumber', 'serialNumber'])
            g.add_metric([self.appliance, str(rss['DiskNumber']), rss['SN']], rss['TotalWritten'] * 1073742000)
            yield g

            g = GaugeMetricFamily('mqa_raid_ssd_life_left', 'Estimate of the remaining drive lifetime', labels=['appliance', 'diskNumber', 'serialNumber'])
            g.add_metric([self.appliance, str(rss['DiskNumber']), rss['SN']], rss['LifeLeft'])
            yield g

        