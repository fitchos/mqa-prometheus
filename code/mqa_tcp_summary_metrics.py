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

"""This module implements the MQ Appliance TCP summary metrics collector"""

import requests
import json

from datetime import datetime
from mqalib import call_rest_api
from prometheus_client.core import GaugeMetricFamily

class MQATCPSummaryMetrics(object):
    """MQ Appliance TCP summary metrics collector"""

    def __init__(self, appliance, ip, port, auth, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.auth = auth
        self.timeout = timeout

    def collect(self):
        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/TCPSummary', self.ip, self.port, self.auth, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        g = GaugeMetricFamily('mqa_tcp_connections_established', 'The number of TCP connections in the established state. Connections in this state have completed all handshakes and can transfer data in either direction', labels=['appliance'])
        g.add_metric([self.appliance], data['TCPSummary']['established'])
        yield g

        g = GaugeMetricFamily('mqa_tcp_connections_syn_sent', 'The number of TCP connections in the syn-sent state. Connections in this state are waiting for a matching connection request after sending a connection request', labels=['appliance'])
        g.add_metric([self.appliance], data['TCPSummary']['syn_sent'])
        yield g

        g = GaugeMetricFamily('mqa_tcp_connections_syn_received', 'The number of TCP connections in the syn-received state. Connections in this state are waiting for a confirming connection request acknowledgment after both receiving and sending a connection request', labels=['appliance'])
        g.add_metric([self.appliance], data['TCPSummary']['syn_received'])
        yield g

        g = GaugeMetricFamily('mqa_tcp_connections_fin_wait_1', 'The number of TCP connections in the fin-wait-1 state. Connections in this state are waiting for a connection termination request from the remote TCP or an acknowledgment of the connection termination request previously sent', labels=['appliance'])
        g.add_metric([self.appliance], data['TCPSummary']['fin_wait_1'])
        yield g

        g = GaugeMetricFamily('mqa_tcp_connections_fin_wait_2', 'The number of TCP connections in the fin-wait-2 state. Connections in this state are waiting for a connection termination request from the remote TCP', labels=['appliance'])
        g.add_metric([self.appliance], data['TCPSummary']['fin_wait_2'])
        yield g

        g = GaugeMetricFamily('mqa_tcp_connections_time_wait', 'The number of TCP connections in the time-wait state. Connections in this state are waiting for enough time to pass to be sure that the remote TCP received the acknowledgment of its connection termination request', labels=['appliance'])
        g.add_metric([self.appliance], data['TCPSummary']['time_wait'])
        yield g

        g = GaugeMetricFamily('mqa_tcp_connections_closed', 'The number of TCP connections in the closed state. This state represents no connection state at all', labels=['appliance'])
        g.add_metric([self.appliance], data['TCPSummary']['closed'])
        yield g

        g = GaugeMetricFamily('mqa_tcp_connections_close_wait', 'The number of TCP connections in the close-wait state. Connections in this state are waiting for a connection termination request from the local user', labels=['appliance'])
        g.add_metric([self.appliance], data['TCPSummary']['close_wait'])
        yield g

        g = GaugeMetricFamily('mqa_tcp_connections_last_ack', 'The number of TCP connections in the last-ack state. Connections in this state are waiting for an acknowledgment of the connection termination request previously sent to the remote TCP (which includes an acknowledgment of its connection termination request)', labels=['appliance'])
        g.add_metric([self.appliance], data['TCPSummary']['last_ack'])
        yield g

        g = GaugeMetricFamily('mqa_tcp_connections_listen', 'The number of TCP connections in the listen state. Connections in the listen state are waiting for a connection request from any remote TCP and port', labels=['appliance'])
        g.add_metric([self.appliance], data['TCPSummary']['listen'])
        yield g

        g = GaugeMetricFamily('mqa_tcp_connections_closing', 'The number of TCP connections in the closing state. Connections in this state are waiting for a connection termination request acknowledgment from the remote TCP', labels=['appliance'])
        g.add_metric([self.appliance], data['TCPSummary']['closing'])
        yield g