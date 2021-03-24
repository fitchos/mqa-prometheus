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

"""This module implements the MQ Appliance queue managers channels metrics collector"""

import json
import time

from mqalib import call_rest_api
from mqalib import datetime_to_epoch
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily, InfoMetricFamily

class MQAQueueManagersChannelsMetrics(object):
    """MQ Appliance queue managers channels metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):

        start = time.time()

        # Perform REST API call to fetch the list of queue managers
        qm_data = call_rest_api('/ibmmq/rest/v2/admin/qmgr', self.ip, self.port, self.session, self.timeout)
        if qm_data == '':
            return

        command = {
            'type': 'runCommandJSON',
            'command': 'display',
            'qualifier': 'chstatus',
            'name': '*',
            'responseParameters': ['all']
        }

        # For each running queue manager fetch the channels
        total_queue_managers = 0
        total_channels = 0

        for qm in qm_data['qmgr']:

            if qm['state'] == 'running':
                headers = {'Content-type': 'application/json;charset=UTF-8', 'ibm-mq-rest-csrf-token': ''}
                 # v2 call, only available since 9.1.5
                channel_data = call_rest_api('/ibmmq/rest/v2/admin/action/qmgr/' + qm['name'] + '/mqsc', self.ip, self.port, self.session, self.timeout, 'POST', headers, command)
                if channel_data == '':
                    continue

                total_queue_managers += 1

                # Update Prometheus metrics
                for channel in channel_data['commandResponse']:
                    if channel['completionCode'] == 0:

                        total_channels += 1

                        g = GaugeMetricFamily('mqa_qm_channel_running_state', 'The current status of the channel, 1 if the channel is in RUNNING state, 0 otherwise', labels=['appliance', 'qm', 'channel', 'chlType', 'jobName'])
                        g.add_metric([self.appliance, qm['name'], channel['parameters']['channel'], channel['parameters']['chltype'], channel['parameters']['jobname']], 1 if channel['parameters']['status'] == 'RUNNING' else 0)
                        yield g

                        c = CounterMetricFamily('mqa_qm_channel_start_datetime_seconds', 'The datetime on which the channel started in epoch seconds', labels=['appliance', 'qm', 'channel', 'chlType', 'jobName'])
                        c.add_metric([self.appliance, qm['name'], channel['parameters']['channel'], channel['parameters']['chltype'], channel['parameters']['jobname']], datetime_to_epoch(channel['parameters']['chstada'] + ' ' + channel['parameters']['chstati'], '%Y-%m-%d %H.%M.%S'))
                        yield c

                        c = CounterMetricFamily('mqa_qm_channel_last_message_datetime_seconds', 'The datetime on which the last message was sent on the channel in epoch seconds', labels=['appliance', 'qm', 'channel', 'chlType', 'jobName'])
                        c.add_metric([self.appliance, qm['name'], channel['parameters']['channel'], channel['parameters']['chltype'], channel['parameters']['jobname']], datetime_to_epoch(channel['parameters']['lstmsgda'] + ' ' + channel['parameters']['lstmsgti'], '%Y-%m-%d %H.%M.%S'))
                        yield c

                        c = CounterMetricFamily('mqa_qm_channel_messages', 'The number of messages sent on the channel since it started', labels=['appliance', 'qm', 'channel', 'chlType', 'jobName'])
                        c.add_metric([self.appliance, qm['name'], channel['parameters']['channel'], channel['parameters']['chltype'], channel['parameters']['jobname']], channel['parameters']['msgs'])
                        yield c

                        try:
                            remoteQMgr = channel['parameters']['rqmname']
                        except KeyError:
                            remoteQMgr = ''

                        i = InfoMetricFamily('mqa_qm_channel', 'MQ Appliance channel information')
                        i.add_metric(['appliance', 'qm', 'channel', 'chlType', 'jobName', 'status', 'conName', 
                                      'remoteQMgr', 'remoteProduct', 'remoteVersion'], 
                                    {'appliance': self.appliance, 
                                    'qm': qm['name'], 
                                    'channel': channel['parameters']['channel'],
                                    'chlType': channel['parameters']['chltype'],
                                    'jobName': channel['parameters']['jobname'],
                                    'status': channel['parameters']['status'],
                                    'conName': channel['parameters']['conname'],
                                    'remoteQMgr': remoteQMgr,
                                    'remoteProduct': channel['parameters']['rproduct'],
                                    'remoteVersion': channel['parameters']['rversion']})
                        yield i

        g = GaugeMetricFamily('mqa_exporter_queue_managers_current_channels_count', 'Exporter total number of current channels for all running queue managers', labels=['appliance'])
        g.add_metric([self.appliance], total_channels)
        yield g

        g = GaugeMetricFamily('mqa_exporter_queue_managers_channels_elapsed_time_seconds', 'Exporter eleapsed time to collect queue managers channels metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.time() - start)
        yield g


        
