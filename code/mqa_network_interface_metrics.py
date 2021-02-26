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

"""This module implements the MQ Appliance network interface metrics collector"""

import requests
import json

from datetime import datetime
from mqalib import call_rest_api
from prometheus_client.core import CounterMetricFamily, InfoMetricFamily

class MQANetworkInterfaceMetrics(object):
    """MQ Appliance network interface metrics collector"""

    def __init__(self, appliance, ip, port, auth, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.auth = auth
        self.timeout = timeout

    def collect(self):
        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/NetworkInterfaceStatus', self.ip, self.port, self.auth, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        for ni in data['NetworkInterfaceStatus']:

            c = CounterMetricFamily('mqa_network_interface_rx_bytes_total', 'The amount of data successfully received on the interface, which includes MAC framing overhead', labels=['appliance', 'name', 'adminStatus', 'operStatus'])
            c.add_metric([self.appliance, ni['Name'], ni['AdminStatus'], ni['OperStatus']], ni['RxHCBytes'])
            yield c

            c = CounterMetricFamily('mqa_network_interface_rx_packets_total', 'The number of packets successfully received on the interface that were passed up to the network layer for processing', labels=['appliance', 'name', 'adminStatus', 'operStatus'])
            c.add_metric([self.appliance, ni['Name'], ni['AdminStatus'], ni['OperStatus']], ni['RxHCPackets'])
            yield c

            c = CounterMetricFamily('mqa_network_interface_rx_errors_total', 'The number of packets that could not be received due to errors in the packet or in the hardware', labels=['appliance', 'name', 'adminStatus', 'operStatus'])
            c.add_metric([self.appliance, ni['Name'], ni['AdminStatus'], ni['OperStatus']], ni['RxErrors2'])
            yield c

            c = CounterMetricFamily('mqa_network_interface_rx_drops_total', 'The number of received packets that were not in error, but were not passed up to the network layer due to resource constraints', labels=['appliance', 'name', 'adminStatus', 'operStatus'])
            c.add_metric([self.appliance, ni['Name'], ni['AdminStatus'], ni['OperStatus']], ni['RxDrops2'])
            yield c

            c = CounterMetricFamily('mqa_network_interface_tx_bytes_total', 'The amount of data successfully transmitted on the interface, which includes MAC framing overhead', labels=['appliance', 'name', 'adminStatus', 'operStatus'])
            c.add_metric([self.appliance, ni['Name'], ni['AdminStatus'], ni['OperStatus']], ni['TxHCBytes'])
            yield c

            c = CounterMetricFamily('mqa_network_interface_tx_packets_total', 'The number of packets successfully transmitted on the interface', labels=['appliance', 'name', 'adminStatus', 'operStatus'])
            c.add_metric([self.appliance, ni['Name'], ni['AdminStatus'], ni['OperStatus']], ni['TxHCPackets'])
            yield c

            c = CounterMetricFamily('mqa_network_interface_tx_errors_total', 'The number of packets that were not successfully transmitted due to errors on the network or in the hardware', labels=['appliance', 'name', 'adminStatus', 'operStatus'])
            c.add_metric([self.appliance, ni['Name'], ni['AdminStatus'], ni['OperStatus']], ni['TxErrors2'])
            yield c

            c = CounterMetricFamily('mqa_network_interface_tx_drops_total', 'The number of packets that were not transmitted because the network layer was generating packets faster than the physical network could accept them', labels=['appliance', 'name', 'adminStatus', 'operStatus'])
            c.add_metric([self.appliance, ni['Name'], ni['AdminStatus'], ni['OperStatus']], ni['TxDrops2'])
            yield c

            i = InfoMetricFamily('mqa_network_interface', 'MQ Appliance network interface information')
            i.add_metric(['appliance', 'interfaceIndex', 'interfaceType', 'name', 'adminStatus', 'operStatus', 'ipType', 'ip', 'prefixLength', 'macAddress', 'mtu'], 
                      {'appliance': self.appliance, 
                      'interfaceIndex': str(ni['InterfaceIndex']),
                      'interfaceType': ni['InterfaceType'],
                      'name': ni['Name'], 
                      'adminStatus': ni['AdminStatus'], 
                      'operStatus': ni['OperStatus'], 
                      'ipType': ni['IPType'], 
                      'ip': ni['IP'], 
                      'prefixLength': str(ni['PrefixLength']), 
                      'macAddress': ni['MACAddress'], 
                      'mtu': str(ni['MTU'])})
            yield i

