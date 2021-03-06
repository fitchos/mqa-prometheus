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

"""This module implements the MQ Appliance ethernet counters metrics collector"""

import json
import time

from mqalib import call_rest_api
from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily

class MQAEthernetCountersMetrics(object):
    """MQ Appliance ethernet counters metrics collector"""

    def __init__(self, appliance, ip, port, session, timeout):
        self.appliance = appliance
        self.ip = ip
        self.port = port
        self.session = session
        self.timeout = timeout

    def collect(self):

        start = time.time()

        # Perform REST API call to fetch data
        data = call_rest_api('/mgmt/status/default/EthernetCountersStatus', self.ip, self.port, self.session, self.timeout)
        if data == '':
            return

        # Update Prometheus metrics
        for ec in data['EthernetCountersStatus']:

            c = CounterMetricFamily('mqa_ethernet_counters_in_unicast_packets_total', 'The number of unicast packets received on this interface', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['InUnicastPackets'] == '' else float(ec['InUnicastPackets']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_in_multicast_packets_total', 'The number of multicast packets received on this interface', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['InMulticastPackets'] == '' else float(ec['InMulticastPackets']))
            yield c
            
            c = CounterMetricFamily('mqa_ethernet_counters_in_broadcast_packets_total', 'The number of broadcast packets received on this interface', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['InBroadcastPackets'] == '' else float(ec['InBroadcastPackets']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_out_unicast_packets_total', 'The number of unicast packets transmitted on this interface', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['OutUnicastPackets'] == '' else float(ec['OutUnicastPackets']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_out_multicast_packets_total', 'The number of multicast packets transmitted on this interface', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['OutMulticastPackets'] == '' else float(ec['OutMulticastPackets']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_out_broadcast_packets_total', 'The number of broadcast packets transmitted on this interface', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['OutBroadcastPackets'] == '' else float(ec['OutBroadcastPackets']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_in_octets_total', 'The number of bytes received on this interface at the MAC level', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['InOctets'] == '' else float(ec['InOctets']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_out_octets_total', 'The number of bytes transmitted on this interface at the MAC level', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['OutOctets'] == '' else float(ec['OutOctets']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_in_errors_total', 'The total number of receive errors on this interface', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['InErrors'] == '' else float(ec['InErrors']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_out_errors_total', 'The total number of transmit errors on this interface', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['OutErrors'] == '' else float(ec['OutErrors']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_out_discards_total', 'The number of packets not transmitted for flow control reasons', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['OutDiscards'] == '' else float(ec['OutDiscards']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_alignment_errors_total', 'The number of packets received on this interface that were not an integral number of bytes in length', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['AlignmentErrors'] == '' else float(ec['AlignmentErrors']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_fcs_errors_total', 'The number of packets received on this interface with an invalid Frame Check Sequence (checksum). This does not include FCS errors on packets that were too long or too short', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['FCSErrors'] == '' else float(ec['FCSErrors']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_single_collision_frames_total', 'The number of packets successfully transmitted on this interface after a single collision. This can only happen when the interface is running in Half-Duplex mode', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['SingleCollisionFrames'] == '' else float(ec['SingleCollisionFrames']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_multiple_collision_frames_total', 'The number of packets successfully transmitted on this interface after multiple collisions, but less than 16 collisions. This can only happen when the interface is running in Half-Duplex mode', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['MultipleCollisionFrames'] == '' else float(ec['MultipleCollisionFrames']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_sqe_test_errors_total', 'The number of times that an SQE test error was encountered. This only can happen when the link is operating in 10BASE-T Half-Duplex', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['SQETestErrors'] == '' else float(ec['SQETestErrors']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_deferred_transmissions_total', 'The number of frames for which the first transmission attempt was deferred because the medium was busy. This can only happen when the interface is running in Half-Duplex mode', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['DeferredTransmissions'] == '' else float(ec['DeferredTransmissions']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_late_collisions_total', 'The number of times that a collision was detected later than one slot time after the transmission of a packet. This can only happen when the interface is running in Half-Duplex mode', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['LateCollisions'] == '' else float(ec['LateCollisions']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_excessive_collisions_total', 'The number of times that transmission of a packet failed because it encountered sixteen collisions in a row. This can only happen when the interface is running in Half-Duplex mode', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['ExcessiveCollisions'] == '' else float(ec['ExcessiveCollisions']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_internal_mac_transmit_errors_total', 'The number of times that transmission of packets failed due to errors inside the MAC layer of the Ethernet interface. These may be due to temporary resource limitations', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['InternalMacTransmitErrors'] == '' else float(ec['InternalMacTransmitErrors']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_carrier_sense_errors_total', 'The number transmitted packets during which there were failures of carrier sense. This can only happen when the interface is running in Half-Duplex mode', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['CarrierSenseErrors'] == '' else float(ec['CarrierSenseErrors']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_frame_too_shorts_total', 'The number of received packets that were shorter than 64 bytes. This can be the result of a collision. Such packages are also known as runts', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['FrameTooShorts'] == '' else float(ec['FrameTooShorts']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_frame_too_longs_total', 'The number of received packets that were longer than the configured MTU. This can be the result of a collision, as well as due to incompatible configuration', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['FrameTooLongs'] == '' else float(ec['FrameTooLongs']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_internal_mac_receive_errors_total', 'The number of times that reception of packets failed due to errors inside the MAC layer of the Ethernet interface. These may be due to temporary resource limitations', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['InternalMacReceiveErrors'] == '' else float(ec['InternalMacReceiveErrors']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_in_pause_frames_total', 'The number of pause frames received', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['InPauseFrames'] == '' else float(ec['InPauseFrames']))
            yield c

            c = CounterMetricFamily('mqa_ethernet_counters_out_pause_frames_total', 'The number of pause frames transmitted', labels=['appliance', 'name'])
            c.add_metric([self.appliance, ec['Name']], 0.0 if ec['OutPauseFrames'] == '' else float(ec['OutPauseFrames']))
            yield c

        g = GaugeMetricFamily('mqa_exporter_ethernet_counters_elapsed_time_seconds', 'Exporter eleapsed time to collect ethernet counters metrics', labels=['appliance'])
        g.add_metric([self.appliance], time.time() - start)
        yield g
