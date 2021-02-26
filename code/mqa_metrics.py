#!/usr/bin/env python

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

"""
This module is the Prometheus exporter that collects all the metrics
for a specific MQ Appliance.
"""

import argparse
import logging
import sys
import time

from getpass import getpass
from logging.handlers import RotatingFileHandler
from mqa_active_users_metrics import MQAActiveUsersMetrics
from mqa_environmental_fan_sensors_metrics import MQAEnvironmentalFanSensorsMetrics
from mqa_environmental_sensors_metrics import MQAEnvironmentalSensorsMetrics
from mqa_ethernet_counters_metrics import MQAEthernetCountersMetrics
from mqa_failure_notification_metrics import MQAFailureNotificationMetrics
from mqa_file_system_metrics import MQAFileSystemMetrics
from mqa_information_metrics import MQAInformationMetrics
from mqa_mq_system_recources_metrics import MQAMQSystemResourcesMetrics
from mqa_network_interface_metrics import MQANetworkInterfaceMetrics
from mqa_queue_managers_metrics import MQAQueueManagersMetrics
from mqa_raid_ssd_metrics import MQARaidSsdMetrics
from mqa_system_cpu_metrics import MQASystemCpuMetrics
from mqa_system_memory_metrics import MQASystemMemoryMetrics
from mqa_tcp_summary_metrics import MQATCPSummaryMetrics
from prometheus_client import start_http_server, REGISTRY
from requests import packages


def main():

    # Build parser to handle the command line options
    parser = argparse.ArgumentParser(description='MQ Appliance Prometheus Exporter')
    parser.add_argument('-a', '--appliance',  type=str, required=True, help = 'Name of the appliance') 
    parser.add_argument('-i', '--ip', type=str, required=True, help = 'IP address of the appliance REST API')
    parser.add_argument('-hp', '--httpPort', type=int, default=8000, help = 'Port number of the exported HTTP server (default: 8000)')
    parser.add_argument('-l', '--log', type=str, help = 'Name of the log file (defaults to STDOUT)')
    parser.add_argument('-ln', '--lognumbers', type=int, default=10, help = 'Number of logs in a rotation (defaults to 10)')
    parser.add_argument('-ls', '--logsize', type=int, default=10485760, help = 'Size of logs in bytes (defaults to 10MB - 10485760)')
    parser.add_argument('-p', '--port', type=str, required=True, help = 'Port number of the appliance REST API')
    parser.add_argument('-t', '--timeout', type=int, required=False, default=15, help = 'Timeout in seconds to perform the REST API call (default: 15)')
    parser.add_argument('-u', '--user', type=str, required=True, help = 'User to login to the appliance')
    parser.add_argument('-x', '--pw', type=str, required=False, help = 'Password to login to the appliance')

    # Display usage if needed
    if len(sys.argv) < 3:
       parser.print_help(sys.stderr)
       sys.exit(1)

    # Process command line options
    args = parser.parse_args()

    # Prompt for the password
    while args.pw == None:
        try:
            pw = getpass('password: ')
            pw = pw.strip()
            if len(pw) > 0:
                args.pw = pw
        except Exception as e:
            print('Error occurred while getting password: ' + e)
            sys.exit(1)

    # Configure the logger
    if args.log is None:
        logging.basicConfig(stream=sys.stdout, 
            level=logging.INFO, 
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt='%Y-%m-%dT%H:%M:%S')
    else:
        logging.basicConfig(handlers=[RotatingFileHandler(args.log, maxBytes=args.logsize, backupCount=args.lognumbers)], 
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt='%Y-%m-%dT%H:%M:%S')

    logging.info('MQ Appliance Prometheus Exporter started on HTTP port ' + str(args.httpPort))
    logging.info('MQ Appliance monitored is ' + args.appliance + ' at ' + args.ip + '(' + str(args.port) + ')')

    # Register metric collectors
    REGISTRY.register(MQAActiveUsersMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQAEnvironmentalFanSensorsMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQAEnvironmentalSensorsMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQAEthernetCountersMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQAFailureNotificationMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQAFileSystemMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQAInformationMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQAMQSystemResourcesMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQANetworkInterfaceMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQAQueueManagersMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQARaidSsdMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQASystemCpuMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQASystemMemoryMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))
    REGISTRY.register(MQATCPSummaryMetrics(args.appliance, args.ip, args.port, (args.user, args.pw), args.timeout))

    # Start the HTTP server serving the metrics
    start_http_server(args.httpPort)

    while True:
        time.sleep(5)

if __name__ == '__main__':
    main()
