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

from logging.handlers import RotatingFileHandler
from mqa_active_users_metrics import MQAActiveUsersMetrics
from mqa_current_sensors_metrics import MQACurrentSensorsMetrics
from mqa_environmental_fan_sensors_metrics import MQAEnvironmentalFanSensorsMetrics
from mqa_environmental_sensors_metrics import MQAEnvironmentalSensorsMetrics
from mqa_ethernet_counters_metrics import MQAEthernetCountersMetrics
from mqa_exporter_information_metrics import MQAExporterInformationMetrics
from mqa_failure_notification_metrics import MQAFailureNotificationMetrics
from mqa_file_system_metrics import MQAFileSystemMetrics
from mqa_information_metrics import MQAInformationMetrics
from mqa_ipmi_sel_events_metrics import MQAIPMISelEventsMetrics
from mqa_log_targets_metrics import MQALogTargetsMetrics
from mqa_mq_system_recources_metrics import MQAMQSystemResourcesMetrics
from mqa_network_interfaces_metrics import MQANetworkInterfacesMetrics
from mqa_other_sensors_metrics import MQAOtherSensorsMetrics
from mqa_queue_managers_channels_metrics import MQAQueueManagersChannelsMetrics
from mqa_queue_managers_metrics import MQAQueueManagersMetrics
from mqa_queue_managers_queues_metrics import MQAQueueManagersQueuesMetrics
from mqa_raid_battery_module_metrics import MQARaidBatteryModuleMetrics
from mqa_raid_physical_drive_metrics import MQARaidPhysicalDriveMetrics
from mqa_raid_ssd_metrics import MQARaidSsdMetrics
from mqa_system_cpu_metrics import MQASystemCpuMetrics
from mqa_system_memory_metrics import MQASystemMemoryMetrics
from mqa_tcp_summary_metrics import MQATCPSummaryMetrics
from mqa_temperature_sensors_metrics import MQATemperatureSensorsMetrics
from mqa_voltage_sensors_metrics import MQAVoltageSensorsMetrics
from mqalib import get_password
from mqalib import get_version
from mqalib import init_rest_api
from prometheus_client import start_http_server, REGISTRY
from requests import packages

if sys.version_info.major == 2:
    from ConfigParser import ConfigParser, NoOptionError, NoSectionError
else:
    from configparser import ConfigParser, NoOptionError, NoSectionError


def main():

    # Build parser to handle the command line options
    parser = argparse.ArgumentParser(description='MQ Appliance Prometheus Exporter - ' + get_version())
    parser.add_argument('-a', '--appliance',  type=str, required=True, help = 'Name of the appliance')
    parser.add_argument('-c', '--config',  type=str, required=False, help = 'Name of the exporter configuration file (INI)') 
    parser.add_argument('-i', '--ip', type=str, required=True, help = 'IP address or DNS of the appliance REST API')
    parser.add_argument('-hp', '--httpPort', type=int, default=8000, help = 'Port number of the exported HTTP server (default: 8000)')
    parser.add_argument('-l', '--log', type=str, help = 'Name of the log file (defaults to STDOUT)')
    parser.add_argument('-ln', '--lognumbers', type=int, default=10, help = 'Number of logs in a rotation (defaults to 10)')
    parser.add_argument('-ls', '--logsize', type=int, default=10485760, help = 'Size of logs in bytes (defaults to 10MB - 10485760)')
    parser.add_argument('-p', '--port', type=str, default=5554, help = 'Port number of the appliance REST API (default: 5554)')
    parser.add_argument('-t', '--timeout', type=int, required=False, default=15, help = 'Timeout in seconds to perform the REST API call (default: 15)')
    parser.add_argument('-u', '--user', type=str, required=True, help = 'User to login to the appliance')
    parser.add_argument('-x', '--pw', type=str, required=False, help = 'Password to login to the appliance')

    # Display usage if needed
    if len(sys.argv) < 3:
       parser.print_help(sys.stderr)
       sys.exit(1)

    # Process command line options
    args = parser.parse_args()

    if args.log != None:
        args.log = args.log.replace('\\', '/')

    # Prompt for the password
    if args.pw == None:
        args.pw = get_password()

    # Configure the logger
    if args.log is None:
        logging.basicConfig(stream=sys.stdout, 
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S')
    else:
        if sys.version[:1] == '3':
            # Python 3 logging, supports log rotation
            logging.basicConfig(handlers=[RotatingFileHandler(args.log, maxBytes=args.logsize, backupCount=args.lognumbers)], 
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - %(message)s",
                datefmt='%Y-%m-%dT%H:%M:%S')
        else:
            # Python 2 logging, does not support log rotation
            logging.basicConfig(filename=args.log, filemode='a', 
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%dT%H:%M:%S')
        
    logging.info('MQ Appliance Prometheus Exporter ' + get_version() + ' started on HTTP port ' + str(args.httpPort))
    logging.info('MQ Appliance monitored is ' + args.appliance + ' at ' + args.ip + '(' + str(args.port) + ')')

    # Read exporter configuration file
    if args.config != None:
        config = ConfigParser()
        config.read(args.config)
        
    # Initialize HTTPS session
    session = init_rest_api(args.ip, args.port, (args.user, args.pw), args.timeout)

    # Register metric collectors
    try:
        if args.config == None or config.getboolean('collectors', 'appliance_information'):
            REGISTRY.register(MQAInformationMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'active_users'):
            REGISTRY.register(MQAActiveUsersMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'current_sensors'):   
            REGISTRY.register(MQACurrentSensorsMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'environmental_fan_sensors'):
            REGISTRY.register(MQAEnvironmentalFanSensorsMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'environmental_sensors'):
            REGISTRY.register(MQAEnvironmentalSensorsMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'ethernet_counters'):
            REGISTRY.register(MQAEthernetCountersMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'exporters_information'):
            REGISTRY.register(MQAExporterInformationMetrics(args.appliance))
        if args.config == None or config.getboolean('collectors', 'failure_notification'):
            REGISTRY.register(MQAFailureNotificationMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'file_system'):
            REGISTRY.register(MQAFileSystemMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'ipmi_sel_events'):
            REGISTRY.register(MQAIPMISelEventsMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'log_targets'):
            REGISTRY.register(MQALogTargetsMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'mq_system_resources'):
            REGISTRY.register(MQAMQSystemResourcesMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'network_interfaces'):
            REGISTRY.register(MQANetworkInterfacesMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'other_sensors'):
            REGISTRY.register(MQAOtherSensorsMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'system_cpu'):
            REGISTRY.register(MQASystemCpuMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'queue_managers'):
            REGISTRY.register(MQAQueueManagersMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'queue_managers_channels'):
            REGISTRY.register(MQAQueueManagersChannelsMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'queue_managers_queues'):
            REGISTRY.register(MQAQueueManagersQueuesMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'raid_battery_module'):
            REGISTRY.register(MQARaidBatteryModuleMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'raid_physical_drive'):
            REGISTRY.register(MQARaidPhysicalDriveMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'raid_ssd'):
            REGISTRY.register(MQARaidSsdMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'system_memory'):
            REGISTRY.register(MQASystemMemoryMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'tcp_summary'):
            REGISTRY.register(MQATCPSummaryMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'temperature_sensors'):
            REGISTRY.register(MQATemperatureSensorsMetrics(args.appliance, args.ip, args.port, session, args.timeout))
        if args.config == None or config.getboolean('collectors', 'voltage_sensors'):
            REGISTRY.register(MQAVoltageSensorsMetrics(args.appliance, args.ip, args.port, session, args.timeout))
    except NoSectionError as err:
        logging.error('Invalid exporter configuration file \'' + args.config + '\', ' + str(err))
        logging.info('Exporter has terminated')
        sys.exit(1)
    except NoOptionError as err:
        logging.error('Invalid exporter configuration file \'' + args.config + '\', ' + str(err))
        logging.info('Exporter has terminated')
        sys.exit(1)

    # Start the HTTP server serving the metrics
    start_http_server(args.httpPort)

    while True:
        time.sleep(5)

if __name__ == '__main__':
    main()
