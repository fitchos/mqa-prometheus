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

"""This module implements the MQ Appliance exporter information metrics collector"""

import time

from mqalib import get_version
from mqalib import datetime_to_epoch
from prometheus_client.core import CounterMetricFamily, InfoMetricFamily

class MQAExporterInformationMetrics(object):
    """MQ Appliance exporter information metrics collector"""

    def __init__(self, appliance):
        self.appliance = appliance

    def collect(self):

        # Collect exporter information
        version = get_version()
        local_time = time.localtime()
        formatted_local_time = time.strftime('%Y-%m-%d %H.%M.%S', local_time)

        try:
            if local_time[8]:
                local_tzname = time.tzname[1]
            else:
                local_tzname = time.tzname[0]
        except AttributeError:
            local_tzname = 'UNKNOWN'

        # Update Prometheus metrics
        c = CounterMetricFamily('mqa_exporter_current_datetime_seconds', 'The current date and time of the server on which the exporter is running in epoch seconds ', labels=['appliance'])
        c.add_metric([self.appliance], datetime_to_epoch(formatted_local_time, '%Y-%m-%d %H.%M.%S'))
        yield c

        i = InfoMetricFamily('mqa_exporter', 'MQ Appliance exporter information')
        i.add_metric(['appliance', 'version', 'localTimezone'],
                      {'appliance': self.appliance, 'version': version, 'localTimezone': local_tzname})
        yield i
