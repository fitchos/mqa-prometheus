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

"""This module implements the MQ Appliance queue managers queues metrics collector"""

import json
import time

from mqalib import call_rest_api
from mqalib import datetime_to_epoch
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

class MQAQueueManagersQueuesMetrics(object):
    """MQ Appliance queue managers queues metrics collector"""

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
            'qualifier': 'qstatus',
            'name': '*',
            'responseParameters': ['curdepth', 'ipprocs', 'opprocs', 'curfsize', 'curmaxfs', 'lgetdate', 'lgettime', 'lputdate', 'lputtime', 'monq','msgage', 'qtime', 'uncom']
        }

        # For each running queue manager fetch the queues
        total_queue_managers = 0
        total_queues = 0

        for qm in qm_data['qmgr']:

            if qm['state'] == 'running':
                headers = {'Content-type': 'application/json;charset=UTF-8', 'ibm-mq-rest-csrf-token': ''}
                 # v2 call, only available since 9.1.5
                queue_data = call_rest_api('/ibmmq/rest/v2/admin/action/qmgr/' + qm['name'] + '/mqsc', self.ip, self.port, self.session, self.timeout, 'POST', headers, command)
                if queue_data == '':
                    continue

                total_queue_managers += 1

                # Update Prometheus metrics
                for queue in queue_data['commandResponse']:
                    if queue['completionCode'] == 0:

                        total_queues += 1

                        g = GaugeMetricFamily('mqa_qm_queue_current_depth', 'The current depth of the queue, that is, the number of messages on the queue, including both committed messages and uncommitted messages', labels=['appliance', 'qm', 'queue'])
                        g.add_metric([self.appliance, qm['name'], queue['parameters']['queue']], queue['parameters']['curdepth'])
                        yield g

                        g = GaugeMetricFamily('mqa_qm_queue_input_procs', 'The number of handles that are currently open for input for the queue (either input-shared or input-exclusive)', labels=['appliance', 'qm', 'queue'])
                        g.add_metric([self.appliance, qm['name'], queue['parameters']['queue']], queue['parameters']['ipprocs'])
                        yield g

                        g = GaugeMetricFamily('mqa_qm_queue_output_procs', 'The number of handles that are currently open for output for the queue', labels=['appliance', 'qm', 'queue'])
                        g.add_metric([self.appliance, qm['name'], queue['parameters']['queue']], queue['parameters']['opprocs'])
                        yield g

                        g = GaugeMetricFamily('mqa_qm_queue_message_age_seconds', 'Age, in seconds, of the oldest message on the queue', labels=['appliance', 'qm', 'queue'])
                        g.add_metric([self.appliance, qm['name'], queue['parameters']['queue']], 0 if queue['parameters']['msgage'] == '' else queue['parameters']['msgage'])
                        yield g

                        if queue['parameters']['uncom'] == 'YES':
                            uncommitted_messages = 1
                        elif queue['parameters']['uncom'] == 'NO':
                            uncommitted_messages = 0
                        else:
                            uncommitted_messages = queue['parameters']['uncom']

                        g = GaugeMetricFamily('mqa_qm_queue_uncommitted_messages', 'The number of uncommitted changes (puts and gets) pending for the queue', labels=['appliance', 'qm', 'queue'])
                        g.add_metric([self.appliance, qm['name'], queue['parameters']['queue']], uncommitted_messages)
                        yield g

                        queue_time = queue['parameters']['qtime']

                        if queue_time == ' , ':
                            q_time_small_sample = -1
                            q_time_large_sample = -1
                        else:
                            q_time_small_sample = float(queue_time[:queue_time.find(',')])
                            q_time_large_sample = float(queue_time[queue_time.find(',') + 1:])

                        g = GaugeMetricFamily('mqa_qm_queue_time_small_sample_seconds', 'Interval, in seconds, between messages being put on the queue and then being destructively read. A value based on the last few messages processed', labels=['appliance', 'qm', 'queue'])
                        g.add_metric([self.appliance, qm['name'], queue['parameters']['queue']], q_time_small_sample / 1000000)
                        yield g

                        g = GaugeMetricFamily('mqa_qm_queue_time_large_sample_seconds', 'Interval, in seconds, between messages being put on the queue and then being destructively read. A value based on a larger sample of the recently processed messages', labels=['appliance', 'qm', 'queue'])
                        g.add_metric([self.appliance, qm['name'], queue['parameters']['queue']], q_time_large_sample / 1000000)
                        yield g

                        current_file_size = 0
                        current_max_file_size = 0
                        try:
                            # Fields only available since 9.1.5
                            current_file_size = queue['parameters']['curfsize'] * 1000000
                            g = GaugeMetricFamily('mqa_qm_queue_current_file_size_bytes', 'The current size of the queue file in bytes, rounded up to the nearest megabyte', labels=['appliance', 'qm', 'queue'])
                            g.add_metric([self.appliance, qm['name'], queue['parameters']['queue']], current_file_size)
                            yield g

                            current_max_file_size = queue['parameters']['curmaxfs'] * 1000000
                            g = GaugeMetricFamily('mqa_qm_queue_current_max_file_size_bytes', 'The current maximum size in bytes the queue file can grow to, rounded up to the nearest megabyte, given the current block size in use on a queue', labels=['appliance', 'qm', 'queue'])
                            g.add_metric([self.appliance, qm['name'], queue['parameters']['queue']], current_max_file_size)
                            yield g
                        except KeyError:
                            pass

                        c = CounterMetricFamily('mqa_qm_queue_last_get_datetime_seconds', 'The datetime on which the last message was retrieved from the queue since the queue manager started in epoch seconds', labels=['appliance', 'qm', 'queue'])
                        c.add_metric([self.appliance, qm['name'], queue['parameters']['queue']], datetime_to_epoch(queue['parameters']['lgetdate'] + ' ' + queue['parameters']['lgettime'], '%Y-%m-%d %H.%M.%S'))
                        yield c

                        c = CounterMetricFamily('mqa_qm_queue_last_put_datetime_seconds', 'The datetime on which the last message was put to the queue since the queue manager started in epoch seconds', labels=['appliance', 'qm', 'queue'])
                        c.add_metric([self.appliance, qm['name'], queue['parameters']['queue']], datetime_to_epoch(queue['parameters']['lgetdate'] + ' ' + queue['parameters']['lgettime'], '%Y-%m-%d %H.%M.%S'))
                        yield c

        g = GaugeMetricFamily('mqa_exporter_queue_managers_queues_elapsed_time_seconds', 'Exporter eleapsed time to collect queue managers queues metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.time() - start)
        yield g

        g = GaugeMetricFamily('mqa_exporter_queue_managers_total', 'Exporter total number of running queue managers', labels=['appliance'])
        g.add_metric([self.appliance], total_queue_managers)
        yield g

        g = GaugeMetricFamily('mqa_exporter_queue_managers_queues_total', 'Exporter total number of queues for all running queue managers', labels=['appliance'])
        g.add_metric([self.appliance], total_queues)
        yield g
