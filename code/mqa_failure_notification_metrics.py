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

"""This module implements the MQ Appliance failure notification metrics collector"""

import json
import time

from mqalib import call_rest_api
from prometheus_client.core import InfoMetricFamily, GaugeMetricFamily

class MQAFailureNotificationMetrics(object):
    """MQ Appliance failure notification metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):

        start = time.perf_counter()

        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/FailureNotificationStatus2', self.ip, self.port, self.session, self.timeout)

        if data == '':
            return

        failureNotifications = []

        if type(data['FailureNotificationStatus2']) is dict:
            failureNotifications.append(data['FailureNotificationStatus2'])
        else:
            failureNotifications = data['FailureNotificationStatus2']


        # Update Prometheus metrics
        for fn in failureNotifications:

            i = InfoMetricFamily('mqa_failure_notification', 'MQ Appliance failure notification')
            i.add_metric(['appliance', 'date', 'reason', 'uploadStatus', 'location'], 
                      {'appliance': self.appliance, 'date': fn['Date'], 'reason': fn['Reason'],
                      'uploadStatus': fn['UploadStatus'], 'location': fn['Location']})
            yield i

        g = GaugeMetricFamily('mqa_exporter_failure_notification_elapsed_time_seconds', 'Exporter eleapsed time to collect failure notification metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.perf_counter() - start)
        yield g
