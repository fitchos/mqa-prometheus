# mqa-prometheus
This project provides a Prometheus Exporter for the IBM MQ Appliance. 

![IBM MQ Appliance](/images/IBM_MQ_Appliance.png)

## WARNING
The **main** branch is the development branch which may not be stable!
Instead download the latest release.

## Prerequisites
The following are prerequisites to run the exporter:
1. Prometheus (https://prometheus.io/download/)
2. Grafana (https://grafana.com/get/?plcmt=top-nav&cta=downloads)
3. Grafana Clock plugin
    ```
      grafana-cli plugins install grafana-clock-panel
    ```
4. Python 3.x or 2.x (https://www.python.org/downloads/)
5. Prometheus Python client library
    ```
      pip install prometheus-client
    ```
6. Python Requests library
    ```
      pip install requests
    ```
7. MQ Appliance REST API must be enabled

## Getting Started
You must run a separate exporter for each MQ Appliance you want to collect metrics for, but it
is possible to run more than one exporter against an MQ Appliance if you want to split collectors
across exporters to lessen the collection times and meet specific Prometheus scrape times. 

Certain collectors, like the MQ queues and channels collectors may take some time to run depending
on the number of queue managers running on an MQ Appliance, and the number of queues and channels in
use on each queue manager. These two collectors may benefit to run in their own separate exporter.

mqa_metrics.py is the name of the module to run an exporter. Only basic authentication is
currently supported.

**Note: if you use Python 2 and log to a file, you need to use an external mechanism to rotate the logs**

```
Usage: mqa_metrics.py [-h] -a APPLIANCE [-c CONFIG] -i IP [-hp HTTPPORT]
                      [-l LOG] [-ln LOGNUMBERS] [-ls LOGSIZE] [-p PORT]
                      [-t TIMEOUT] -u USER [-x PW]

MQ Appliance Prometheus Exporter - vx.x

optional arguments:
  -h, --help            show this help message and exit
  -a APPLIANCE, --appliance APPLIANCE
                        Name of the appliance
  -c CONFIG, --config CONFIG
                        Name of the exporter configuration file (INI)
  -i IP, --ip IP        IP address or DNS of the appliance REST API
  -hp HTTPPORT, --httpPort HTTPPORT
                        Port number of the exported HTTP server (default:
                        9813)
  -l LOG, --log LOG     Name of the log file (defaults to STDOUT)
  -ln LOGNUMBERS, --lognumbers LOGNUMBERS
                        Number of logs in a rotation (defaults to 10)
  -ls LOGSIZE, --logsize LOGSIZE
                        Size of logs in bytes (defaults to 10MB - 10485760)
  -p PORT, --port PORT  Port number of the appliance REST API (default: 5554)
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in seconds to perform the REST API call
                        (default: 15)
  -u USER, --user USER  User to login to the appliance
  -x PW, --pw PW        Password to login to the appliance
```

### Sample commands to run an exporter
Run an exporter with logging output to STDOUT and password being prompted on the command line

```
mqa_metrics.py -a MQAPROD1 -i 192.168.28.250 -p 5554 -u admin -hp 9813
```

Run an exporter with logging output to a file using all logging defaults

```
mqa_metrics.py -a MQAPROD1 -i 192.168.28.250 -p 5554 -u admin -x mypassword -hp 9813 -l mqaprod1.log 
```

Run a second exporter (note: the HTTPPORT must be different)

```
mqa_metrics.py -a MQAPROD2 -i 192.168.28.210 -p 5554 -u admin -x mypassword -hp 9814 -l mqaprod2.log
```

Run an exporter with a configuration file to select which metric collectors are running

```
mqa_metrics.py -a MQAPROD3 -i 192.168.28.210 -p 5554 -u admin -x mypassword -hp 9815 -c exporters.cfg
```

The configuration looks like this:
```
# Exporters configuration file

# List of available metrics collectors - set to true or false to run or not run a collector
[collectors]
appliance_information = true
active_users = true
current_sensors = false
environmental_fan_sensors = true
environmental_sensors = true
ethernet_counters = true
failure_notification = true
file_system = true
ipmi_sel_events = false
log_targets = true
mq_system_resources = true
network_interfaces = true
other_sensors = true
queue_managers = true
raid_ssd = true
system_cpu = true
system_memory = true
tcp_summary = true
temperature_sensors = false
voltage_sensors = false
```

When no configuration file is specified, all metric collectors run by default.

**IMPORTANT:** If you run multiple exporters for an appliance to split the number of
collectors across more than one exporter, ensure that the configuration files used do
not duplicate the collectors run, otherwise this will lead to duplicate metrics series
in Prometheus.

### Utilities to manage the operation of the exporters
Please take note that as of the latest release, the utilities can only be used to 
manage exporters when ONLY one (1) exporter is used per appliance. 

Three utilities are available to:

1. Start multiple exporters using a CSV file
2. List the exporters currently running
3. Stop one or more exporters

**Note: Environment variable MQA_EXPORTER_DIRECTORY can be set to a directory name**
**and avoid having to specify the -d parameter on the commands. If the environment**
**variable is not set and the -d parameter is not specified, the directory where the**
**log and PID files are stored is the current directory**

#### Starting multiple exporters
To start multiple exporters build a CSV (comma delimited) file with the following information:

- appliance name
- IP or DNS name of the appliance
- Port number of the REST API
- Port number to serve the metrics to Prometheus
- Timeout value for the REST API calls to the appliance

To start the exporters, use the mqa_start_exporters utility

```
Usage: mqa_start_exporters.py [-h] [-a APPLIANCE] [-c CONFIG] [-d DIRECTORY] -f FILE [-ln LOGNUMBERS] [-ls LOGSIZE] -u USER [-x PW]

MQ Appliance Prometheus Exporter Start Utility - vx.x

optional arguments:
  -h, --help            show this help message and exit
  -a APPLIANCE, --appliance APPLIANCE
                        Name of the appliance
  -c CONFIG, --config CONFIG
                        Name of the exporter configuration file (INI)
  -d DIRECTORY, --directory DIRECTORY
                        Path to directory for PID files (defaults to current directory)
  -f FILE, --file FILE  Name of the file with the exporters configuration (CSV)
  -ln LOGNUMBERS, --lognumbers LOGNUMBERS
                        Number of logs in a rotation (defaults to 10)
  -ls LOGSIZE, --logsize LOGSIZE
                        Size of logs in bytes (defaults to 10MB - 10485760)
  -u USER, --user USER  User to login to the appliance
  -x PW, --pw PW        Password to login to the appliance
```

#### Sample commands to start a list of exporters
```
mqa_start_exporters.py -f my_exporter_list.csv -d \temp -u admin
mqa_start_exporters.py -f my_exporter_list.csv -u admin -c exporters.cfg
```

#### Listing exporters currently running
To list the exporters currently running, use the mqa_list_exporters utility

```
Usage: mqa_list_exporters.py [-h] [-a APPLIANCE] [-d DIRECTORY] [-f FILE]

MQ Appliance Prometheus Exporter List Utility - vx.x

optional arguments:
  -h, --help            show this help message and exit
  -a APPLIANCE, --appliance APPLIANCE
                        Name of the appliance
  -d DIRECTORY, --directory DIRECTORY
                        Path to directory for PID files (defaults to current directory)
  -f FILE, --file FILE  Name of the file with the exporters configuration (CSV)
```

#### Sample commands to list exporters running
```
mqa_list_exporters.py -d \temp
mqa_list_exporters.py -d \temp -a my_appliance
mqa_list_exporters.py -f my_exporters_file.csv
mqa_list_exporters.py -f my_exporters_file.csv -a my_appliance
```

#### Stopping one or more exporters
To stop one or more exporters, use the mqa_stop_exporters utility

```
Usage: mqa_stop_exporters.py [-h] [-a APPLIANCE] [-d DIRECTORY] [-f FILE]

MQ Appliance Prometheus Exporter Stop Utility - vx.x

optional arguments:
  -h, --help            show this help message and exit
  -a APPLIANCE, --appliance APPLIANCE
                        Name of the appliance
  -d DIRECTORY, --directory DIRECTORY
                        Path to directory for PID files (defaults to current directory)
  -f FILE, --file FILE  Name of the file with the exporters configuration (CSV)
```

#### Sample commands to stop one or more exporters
```
mqa_stop_exporters.py -d \temp
mqa_stop_exporters.py -d \temp -a my_appliance
mqa_stop_exporters.py -d \temp -f my_exporters_list.csv
mqa_stop_exporters.py -d \temp -f my_exporters_list.csv -a my_appliance
```

### Available metrics
**Active Users**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_active_users_total | Gauge | Total active users connected to the appliance | appliance, connection |

**Current Sensors**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
|mqa_current_sensors_power_supply_1_in_current_amperes | Gauge | Current going into power supply 1 | appliance, readingStatus |
|mqa_current_sensors_power_supply_1_in_current_upper_critical_threshold_amperes | Gauge | Upper critical threshold for current going into power supply 1 | appliance, readingStatus |
|mqa_current_sensors_power_supply_1_out_current_amperes | Gauge | Current going out power supply 1 | appliance, readingStatus |
|mqa_current_sensors_power_supply_1_out_current_upper_critical_threshold_amperes | Gauge | Upper critical threshold for current going out power supply 1 | appliance, readingStatus |
|mqa_current_sensors_power_supply_2_in_current_amperes | Gauge | Current going into power supply 2 | appliance, readingStatus |
|mqa_current_sensors_power_supply_2_in_current_upper_critical_threshold_amperes | Gauge | Upper critical threshold for current going into power supply 2 | appliance, readingStatus |
|mqa_current_sensors_power_supply_2_out_current_amperes | Gauge | Current going out power supply 2 | appliance, readingStatus |
|mqa_current_sensors_power_supply_2_out_current_upper_critical_threshold_amperes | Gauge | Upper critical threshold for current going out power supply 2 | appliance, readingStatus |

**Environmental Sensors**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_environmental_fan_sensors_fan_speed_rpm | Gauge | The speed of the fan in revolutions per minute (RPM) | appliance, fanID, readingStatus |
| mqa_environmental_fan_sensors_fan_speed_lower_critical_threshold_rpm | Gauge | The lowest allowable reading of the fan speed sensor | appliance, fanID, readingStatus |

**Environmental Fan Sensors**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_environmental_sensors_system_temperature_celsius | Gauge | Ambient temperature | appliance |
| mqa_environmental_sensors_cpu_1_temperature_celsius | Gauge | CPU 1 temperature | appliance |
| mqa_environmental_sensors_cpu_2_temperature_celsius | Gauge | CPU 2 temperature | appliance |
| mqa_environmental_sensors_cpu_1_fan_speed_rpm | Gauge | CPU 1 fan speed | appliance |
| mqa_environmental_sensors_cpu_2_fan_speed_rpm | Gauge | CPU 2 fan speed | appliance |
| mqa_environmental_sensors_chassis_fan_1_speed_rpm | Gauge | Chassis fan 1 speed | appliance |
| mqa_environmental_sensors_chassis_fan_2_speed_rpm | Gauge | Chassis fan 2 speed | appliance |
| mqa_environmental_sensors_chassis_fan_3_speed_rpm | Gauge | Chassis fan 3 speed | appliance |
| mqa_environmental_sensors_33_voltage | Gauge | 3.3 voltage | appliance |
| mqa_environmental_sensors_5_voltage | Gauge | 5 voltage | appliance |
| mqa_environmental_sensors_12_voltage | Gauge | 12 voltage | appliance |

**Ethernet Counters**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_ethernet_counters_in_unicast_packets_total | Counter | The number of unicast packets received on this interface | appliance, name |
| mqa_ethernet_counters_in_multicast_packets_total | Counter | The number of multicast packets received on this interface | appliance, name |
| mqa_ethernet_counters_in_broadcast_packets_total | Counter | The number of broadcast packets received on this interface | appliance, name |
| mqa_ethernet_counters_out_unicast_packets_total | Counter | The number of unicast packets transmitted on this interface | appliance, name |
| mqa_ethernet_counters_out_multicast_packets_total | Counter | The number of multicast packets transmitted on this interface | appliance, name |
| mqa_ethernet_counters_out_broadcast_packets_total | Counter | The number of broadcast packets transmitted on this interface | appliance, name |
| mqa_ethernet_counters_in_octets_total | Counter | The number of bytes received on this interface at the MAC level | appliance, name |
| mqa_ethernet_counters_out_octets_total | Counter | The number of bytes transmitted on this interface at the MAC level | appliance, name |
| mqa_ethernet_counters_in_errors_total | Counter | The total number of receive errors on this interface | appliance, name |
| mqa_ethernet_counters_out_errors_total | Counter | The total number of transmit errors on this interface | appliance, name |
| mqa_ethernet_counters_out_discards_total | Counter | The number of packets not transmitted for flow control reasons | appliance, name |
| mqa_ethernet_counters_alignment_errors_total | Counter | The number of packets received on this interface that were not an integral number of bytes in length | appliance, name |
| mqa_ethernet_counters_fcs_errors_total | Counter | The number of packets received on this interface with an invalid Frame Check Sequence (checksum). This does not include FCS errors on packets that were too long or too short | appliance, name |
| mqa_ethernet_counters_single_collision_frames_total | Counter | The number of packets successfully transmitted on this interface after a single collision. This can only happen when the interface is running in Half-Duplex mode | appliance, name |
| mqa_ethernet_counters_multiple_collision_frames_total | Counter | The number of packets successfully transmitted on this interface after multiple collisions, but less than 16 collisions. This can only happen when the interface is running in Half-Duplex mode | appliance, name |
| mqa_ethernet_counters_sqe_test_errors_total | Counter | The number of times that an SQE test error was encountered. This only can happen when the link is operating in 10BASE-T Half-Duplex | appliance, name |
| mqa_ethernet_counters_deferred_transmissions_total | Counter | The number of frames for which the first transmission attempt was deferred because the medium was busy. This can only happen when the interface is running in Half-Duplex mode | appliance, name |
| mqa_ethernet_counters_late_collisions_total | Counter | The number of times that a collision was detected later than one slot time after the transmission of a packet. This can only happen when the interface is running in Half-Duplex mode | appliance, name |
| mqa_ethernet_counters_excessive_collisions_total | Counter | The number of times that transmission of a packet failed because it encountered sixteen collisions in a row. This can only happen when the interface is running in Half-Duplex mode | appliance, name |
| mqa_ethernet_counters_internal_mac_transmit_errors_total | Counter | The number of times that transmission of packets failed due to errors inside the MAC layer of the Ethernet interface. These may be due to temporary resource limitations | appliance, name |
| mqa_ethernet_counters_carrier_sense_errors_total | Counter | The number transmitted packets during which there were failures of carrier sense. This can only happen when the interface is running in Half-Duplex mode | appliance, name |
| mqa_ethernet_counters_frame_too_shorts_total | Counter | The number of received packets that were shorter than 64 bytes. This can be the result of a collision. Such packages are also known as runts | appliance, name |
| mqa_ethernet_counters_frame_too_longs_total | Counter | The number of received packets that were longer than the configured MTU. This can be the result of a collision, as well as due to incompatible configuration | appliance, name |
| mqa_ethernet_counters_internal_mac_receive_errors_total | Counter | The number of times that reception of packets failed due to errors inside the MAC layer of the Ethernet interface. These may be due to temporary resource limitations | appliance, name |
| mqa_ethernet_counters_in_pause_frames_total | Counter | The number of pause frames received | appliance, name |
| mqa_ethernet_counters_out_pause_frames_total | Counter | The number of pause frames transmitted | appliance, name |

**Exporter Information**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_exporter_info | Info | MQ Appliance exporter information | appliance, version, localTimezone |
| mqa_exporter_current_datetime_seconds_total | Counter | The current date and time of the server on which the exporter is running in epoch seconds | appliance |
| mqa_exporter_active_users_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect active users metrics | appliance |
| mqa_exporter_current_sensors_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect current sensors metrics | appliance |
| mqa_exporter_environmental_fan_sensors_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect environmental fan sensors metrics | appliance |
| mqa_exporter_environmental_sensors_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect environmental sensors metrics | appliance |
| mqa_exporter_ethernet_counters_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect ethernet counters metrics | appliance |
| mqa_exporter_failure_notification_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect failure notification metrics | appliance |
| mqa_exporter_file_system_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect file system metrics | appliance |
| mqa_exporter_mqa_information_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect mqa information metrics | appliance |
| mqa_exporter_ipmi_sel_events_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect ipmi sel events metrics | appliance |
| mqa_exporter_log_targets_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect log targets metrics | appliance |
| mqa_exporter_mq_system_resources_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect mq system resources metrics | appliance |
| mqa_exporter_network_interfaces_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect network interfaces metrics | appliance |
| mqa_exporter_other_sensors_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect other sensors metrics | appliance |
| mqa_exporter_queue_managers_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect queue managers metrics | appliance |
| mqa_exporter_queue_managers_channels_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect queue managers channels metrics | appliance |
| mqa_exporter_queue_managers_queues_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect queue managers queues metrics | appliance |
| mqa_exporter_queue_managers_total | Gauge | Exporter total number of running queue managers | appliance |
| mqa_exporter_queue_managers_current_channels_count | Gauge | Exporter total number of current channels for all running queue managers | appliance |
| mqa_exporter_queue_managers_queues_total | Gauge | Exporter total number of queues for all running queue managers | appliance |
| mqa_exporter_raid_ssd_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect raid ssd metrics | appliance |
| mqa_exporter_system_cpu_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect system cpu metrics | appliance |
| mqa_exporter_system_memory_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect system_memory metrics | appliance |
| mqa_exporter_tcp_summary_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect tcp summary metrics | appliance |
| mqa_exporter_temperature_sensors_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect temperature sensors metrics | appliance |
| mqa_exporter_voltage_sensors_elapsed_time_seconds | Gauge | Exporter eleapsed time to collect voltage sensors metrics | appliance |

**Failure Notifications**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_failure_notification_info | Info | MQ Appliance failure notifications | appliance, date, reason, uploadStatus, location |

**File System**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_file_system_encrypted_bytes_free | Gauge | Free, or unused and available, encrypted storage space on the appliance | appliance |
| mqa_file_system_encrypted_bytes_total | Counter | Total encrypted storage space on the appliance (the maximum capacity) | appliance |
| mqa_file_system_temporary_bytes_free | Gauge | Free, or unused and available, temporary storage space on the appliance | appliance |
| mqa_file_system_temporary_bytes_total | Counter | Total temporary storage space on the appliance | appliance |
| mqa_file_system_internal_bytes_free | Gauge | Free, or unused and available, internal storage space on the appliance | appliance |
| mqa_file_system_internal_bytes_total | Counter | Total internal storage space on the appliance | appliance |

**IPMI SEL Events Information**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_ipmi_sel_events_info | Info | MQ Appliance IPMI SEL events information | appliance, index, timestamp, recordType, sensorType, sensorNumber, sensorName, eventReadingTypeCode, eventData, eventDirection, extra |

**Log Targets**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_log_target_info | Info | MQ Appliance log target information | appliance, name, status |
| mqa_log_target_events_processed_total | Counter | The number of events that this log target processed | appliance, name |
| mqa_log_target_events_dropped_total | Counter | The number of events that this log target dropped because there are too many pending events | appliance, name |
| mqa_log_target_events_pending_total | Counter | The number of pending events for this log target. These events are waiting to be stored at the destination | appliance, name |
| mqa_log_target_memory_requested_total | Counter | The requested memory for this log target. This measurement represents the high watermark of memory requested | appliance, name |

**MQ Appliance Information**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_info | Info | MQ Appliance information | appliance, bootcount, bootuptime, build, builddate, deliverytype, installdate, installeddpos, level, machinetype, modeltype, runningdpos, serial, time, timezone, type, tzspec, uptime, version, watchdogbuild, xmlaccelerator |

**MQ Resources**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_mq_resources_info | Info | MQ Appliance MQ resources information | appliance, haStatus, haPartner |
| mqa_mq_resources_storage_bytes_total | Counter | The total storage in bytes available for IBM MQ data | appliance |
| mqa_mq_resources_storage_bytes_used | Gauge | The amount of IBM MQ storage in use in bytes | appliance |
| mqa_mq_resources_errors_storage_bytes_total | Counter | The total storage in bytes available for IBM MQ error logs | appliance |
| mqa_mq_resources_errors_storage_bytes_used | Gauge | The amount of IBM MQ error log storage in use in bytes | appliance |
| mqa_mq_resources_trace_storage_bytes_total | Counter | The total storage in bytes available for IBM MQ trace | appliance |
| mqa_mq_resources_trace_storage_bytes_used | Gauge | The amount of IBM MQ trace storage in bytes in use | appliance |
| mqa_mq_resources_ha_status | Gauge | HA status of the appliance (0: HA not set, 1: Online, 2: Standby | appliance |
| mqa_mq_resources_ha_partner_status | Gauge | HA status of the partner appliance (0: HA not set, 1: Online, 2: Standby | appliance |

**Network Interfaces**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_network_interface_info | Info | MQ Appliance network interface information | appliance, interfaceIndex, interfaceType, name, adminStatus, operStatus, ipType, ip, prefixLength, macAddress, mtu |
| mqa_network_interface_rx_bytes_total | Counter | The amount of data successfully received on the interface, which includes MAC framing overhead | appliance, adminStatus, name, operStatus |
| mqa_network_interface_rx_packets_total | Counter | The number of packets successfully received on the interface that were passed up to the network layer for processing | appliance, adminStatus, name, operStatus |
| mqa_network_interface_rx_errors_total | Counter | The number of packets that could not be received due to errors in the packet or in the hardware | appliance, adminStatus, name, operStatus |
| mqa_network_interface_rx_drops_total | Counter | The number of received packets that were not in error, but were not passed up to the network layer due to resource constraints | appliance, adminStatus, name, operStatus |
| mqa_network_interface_tx_bytes_total | Counter | The amount of data successfully transmitted on the interface, which includes MAC framing overhead | appliance, adminStatus, name, operStatus |
| mqa_network_interface_tx_packets_total | Counter | The number of packets successfully transmitted on the interface | appliance, adminStatus, name, operStatus |
| mqa_network_interface_tx_errors_total | Counter | The number of packets that were not successfully transmitted due to errors on the network or in the hardware | appliance, adminStatus, name, operStatus |
| mqa_network_interface_tx_drops_total | Counter | The number of packets that were not transmitted because the network layer was generating packets faster than the physical network could accept them | appliance, adminStatus, name, operStatus |

**Other Sensors**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_other_sensor_intrusion_detected | Gauge | Whether an intrusion has been detected | appliance, readingStatus |
| mqa_other_sensor_power_supply_1_ac_lost | Gauge | Whether power supply 1 lost AC | appliance, readingStatus |
| mqa_other_sensor_power_supply_1_not_enabled | Gauge | Whether power supply 1 is not enabled | appliance, readingStatus |
| mqa_other_sensor_power_supply_1_output_failure | Gauge | Whether power supply 1 has an output failure | appliance, readingStatus |
| mqa_other_sensor_power_supply_1_present | Gauge | Whether power supply 1 is present | appliance, readingStatus |
| mqa_other_sensor_power_supply_2_ac_lost | Gauge | Whether power supply 2 lost AC | appliance, readingStatus |
| mqa_other_sensor_power_supply_2_not_enabled | Gauge | Whether power supply 2 is not enabled | appliance, readingStatus |
| mqa_other_sensor_power_supply_2_output_failure | Gauge | Whether power supply 2 has an output failure | appliance, readingStatus |
| mqa_other_sensor_power_supply_2_present | Gauge | Whether power supply 2 is present | appliance, readingStatus |

**Queue Managers**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_queue_manager_info | Info | MQ Appliance queue manager information | appliance, qm, status, haRole, haStatus, drRole, drStatus |
| mqa_queue_manager_cpu_usage | Gauge | The instantaneous CPU usage by the queue manager as a percentage of the CPU load | appliance, qm, status |
| mqa_queue_manager_memory_bytes_used | Gauge | The amount of memory in bytes that is currently in use by the queue manager | appliance, qm, status |
| mqa_queue_manager_fs_bytes_used | Gauge | The amount of file system in bytes that is currently in use by the queue manager | appliance, qm, status |
| mqa_queue_manager_fs_bytes_allocated | Gauge | The amount of file system in bytes allocated for the queue manager | appliance, qm, status |

**Queue Managers Channels**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_qm_channel_info | Info | MQ Appliance channel information | appliance, qm, channel, chlType, jobName, status, conName, remoteQMgr, remoteProduct, remoteVersion |
| mqa_qm_channel_last_message_datetime_seconds | Counter | The datetime on which the last message was sent on the channel in epoch seconds | appliance, qm, channel, chlType, jobName |
| mqa_qm_channel_messages_total | Counter | The number of messages sent on the channel since it started | appliance, qm, channel, chlType, jobName |
| mqa_qm_channel_running_state | Gauge | The current status of the channel, 1 if the channel is in RUNNING state, 0 otherwise | appliance, qm, channel, chlType, jobName |
| mqa_qm_channel_start_datetime_seconds | Counter | The datetime on which the channel started in epoch seconds | appliance, qm, channel, chlType, jobName |

**Queue Managers Queues**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_qm_queue_current_depth | Gauge | The current depth of the queue, that is, the number of messages on the queue, including both committed messages and uncommitted messages | appliance, qm , queue |
| mqa_qm_queue_input_procs | Gauge | The number of handles that are currently open for input for the queue (either input-shared or input-exclusive) | appliance, qm , queue |
| mqa_qm_queue_output_procs | Gauge | The number of handles that are currently open for output for the queue | appliance, qm , queue |
| mqa_qm_queue_message_age_seconds | Gauge | Age, in seconds, of the oldest message on the queue | appliance, qm , queue |
| mqa_qm_queue_uncommitted_messages | Gauge | The number of uncommitted changes (puts and gets) pending for the queue | appliance, qm , queue |
| mqa_qm_queue_time_small_sample_seconds | Gauge | Interval, in seconds, between messages being put on the queue and then being destructively read. A value based on the last few messages processed | appliance, qm , queue |
| mqa_qm_queue_time_large_sample_seconds | Gauge | Interval, in seconds, between messages being put on the queue and then being destructively read. A value based on a larger sample of the recently processed messages | appliance, qm , queue |
| mqa_qm_queue_current_file_size_bytes | Gauge | The current size of the queue file in bytes, rounded up to the nearest megabyte | appliance, qm , queue |
| mqa_qm_queue_current_max_file_size_bytes | Gauge | The current maximum size in bytes the queue file can grow to, rounded up to the nearest megabyte, given the current block size in use on a queue | appliance, qm , queue |
| mqa_qm_queue_last_get_datetime_seconds_total | Counter | The datetime on which the last message was retrieved from the queue since the queue manager started in epoch seconds | appliance, qm , queue |
| mqa_qm_queue_last_put_datetime_seconds_total | Counter | The datetime on which the last message was put to the queue since the queue manager started in epoch seconds | appliance, qm , queue |

**Raid Battery Module**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_raid_battery_module_info | Info | MQ Appliance raid battery module information | appliance, controllerID, batteryType, serial, name, status |
| mqa_raid_battery_module_voltage_volts | Gauge | The actual voltage of the battery in volts | appliance, controllerID, status |
| mqa_raid_battery_module_current_amperes | Gauge | The current that flows through the battery terminals in amperes | appliance, controllerID, status |
| mqa_raid_battery_module_temperature_celsius | Gauge | The temperature of the battery in degrees celsius | appliance, controllerID, status |
| mqa_raid_battery_module_design_capacity_amperes_hour | Gauge | The designed capacity of the battery in ampere-hour | appliance, controllerID, status |
| mqa_raid_battery_module_design_voltage_volts | Gauge | The designed voltage of the battery in volts | appliance, controllerID, status |

**Raid Physical Drive**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_raid_physical_drive_info | Info | MQ Appliance raid physical drive information | appliance, controllerID, deviceID, arrayID, logicalDriveID, logicalDriveName, position, state, interfaceType, interfaceSpeed, sasAddress, vendorID, productID, revision, specificInfo |
| mqa_raid_physical_drive_progress_percent_total | Counter | The current progress percentage of the operation on the physical drive. Operations can be rebuild, copyback, patrol, or clear | appliance, controllerID, deviceID, arrayID, logicalDriveID, position |
| mqa_raid_physical_drive_raw_size_bytes_total | Counter | The exact size of the drive in bytes | appliance, controllerID, deviceID, arrayID, logicalDriveID, position |
| mqa_raid_physical_drive_coerced_size_bytes_total | Counter | The normalized size in megabytes. The value is rounded down to an even multiple, which allows you to swap drives of the same nominal size but might not be the same raw size | appliance, controllerID, deviceID, arrayID, logicalDriveID, position |
| mqa_raid_physical_drive_temperature_celsius | Gauge | The temperature of the hard disk drive in celsius | appliance, controllerID, deviceID, arrayID, logicalDriveID, position |
| | mqa_raid_physical_drive_failure | Gauge | If the hard disk failure state shows Yes, replace this drive as soon as possible to avoid possible data loss | appliance, controllerID, deviceID, arrayID, logicalDriveID, position |

**Raid SSD**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_raid_ssd_bytes_written_total | Counter | The total data in bytes written to the drive since manufacture | appliance, diskNumber, serialNumber |
| mqa_raid_ssd_life_left | Gauge | Estimate of the remaining drive lifetime | appliance, diskNumber, serialNumber |

**System CPU**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_system_cpu_usage | Gauge | The instantaneous CPU usage as a percentage of the CPU load | appliance |
| mqa_system_cpu_load_avg_1m | Gauge | The average CPU load over the last minute | appliance |
| mqa_system_cpu_load_avg_5m | Gauge | The average CPU load over 5 minutes | appliance |
| mqa_system_cpu_load_avg_15m | Gauge | The average CPU load over 15 minutes | appliance |

**System Memory**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_system_memory_memory_usage | Gauge | The instantaneous memory usage as a percentage of the total memory | appliance |
| mqa_system_memory_memory_bytes_total | Counter | The total memory of the system in bytes. The total memory equals the amount of installed memory minus the amount of reserved memory | appliance |
| mqa_system_memory_memory_bytes_used | Gauge | The amount of memory in bytes that is currently in use. The used memory equals the amount of total memory minus the amount of free memory. The used memory does not include any hold memory | appliance |
| mqa_system_memory_memory_bytes_free | Gauge | The amount of memory in bytes that is currently not in use and is therefore available. The free memory value includes any hold memory that is not currently in use | appliance |

**TCP Summary**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_tcp_connections_established | Gauge | The number of TCP connections in the established state. Connections in this state have completed all handshakes and can transfer data in either direction | appliance |
| mqa_tcp_connections_syn_sent | Gauge | The number of TCP connections in the syn-sent state. Connections in this state are waiting for a matching connection request after sending a connection request | appliance |
| mqa_tcp_connections_syn_received | Gauge | The number of TCP connections in the syn-received state. Connections in this state are waiting for a confirming connection request acknowledgment after both receiving and sending a connection request | appliance |
| mqa_tcp_connections_fin_wait_1 | Gauge | The number of TCP connections in the fin-wait-1 state. Connections in this state are waiting for a connection termination request from the remote TCP or an acknowledgment of the connection termination request previously sent | appliance |
| mqa_tcp_connections_fin_wait_2 | Gauge | The number of TCP connections in the fin-wait-2 state. Connections in this state are waiting for a connection termination request from the remote TCP | appliance |
| mqa_tcp_connections_time_wait | Gauge | The number of TCP connections in the time-wait state. Connections in this state are waiting for enough time to pass to be sure that the remote TCP received the acknowledgment of its connection termination request | appliance |
| mqa_tcp_connections_closed | Gauge | The number of TCP connections in the closed state. This state represents no connection state at all | appliance |
| mqa_tcp_connections_close_wait | Gauge | The number of TCP connections in the close-wait state. Connections in this state are waiting for a connection termination request from the local user | appliance |
| mqa_tcp_connections_last_ack | Gauge |The number of TCP connections in the last-ack state. Connections in this state are waiting for an acknowledgment of the connection termination request previously sent to the remote TCP (which includes an acknowledgment of its connection termination request) | appliance |
| mqa_tcp_connections_listen | Gauge | The number of TCP connections in the listen state. Connections in the listen state are waiting for a connection request from any remote TCP and port | appliance |
| mqa_tcp_connections_closing | Gauge | The number of TCP connections in the closing state. Connections in this state are waiting for a connection termination request acknowledgment from the remote TCP seconds | appliance |

**Temperature Sensors**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_temperature_sensor_cpu_dimm_1_channel_a_temperature_celsius | Gauge | CPU DIMM 1 channel A temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_a_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU DIMM 1 channel A in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_a_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU DIMM 1 channel A in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_a_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU DIMM 1 channel A in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_b_temperature_celsius | Gauge | CPU DIMM 1 channel B temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_b_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU DIMM 1 channel B in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_b_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU DIMM 1 channel B in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_b_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU DIMM 1 channel B in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_c_temperature_celsius | Gauge | CPU DIMM 1 channel C temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_c_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU DIMM 1 channel C in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_c_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU DIMM 1 channel C in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_c_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU DIMM 1 channel C in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_d_temperature_celsius | Gauge | CPU DIMM 1 channel D temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_d_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU DIMM 1 channel D in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_d_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU DIMM 1 channel D in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_d_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU DIMM 1 channel D in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_e_temperature_celsius | Gauge | CPU DIMM 1 channel E temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_e_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU DIMM 1 channel E in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_e_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU DIMM 1 channel E in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_e_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU DIMM 1 channel E in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_f_temperature_celsius | Gauge | CPU DIMM 1 channel F temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_f_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU DIMM 1 channel F in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_f_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU DIMM 1 channel F in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_f_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU DIMM 1 channel F in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_g_temperature_celsius | Gauge | CPU DIMM 1 channel G temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_g_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU DIMM 1 channel G in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_g_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU DIMM 1 channel G in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_g_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU DIMM 1 channel G in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_h_temperature_celsius | Gauge | CPU DIMM 1 channel H temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_h_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU DIMM 1 channel H in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_h_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU DIMM 1 channel H in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_h_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU DIMM 1 channel H in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_j_temperature_celsius | Gauge | CPU DIMM 1 channel J temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_j_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU DIMM 1 channel J in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_j_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU DIMM 1 channel J in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_j_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU DIMM 1 channel J in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_k_temperature_celsius | Gauge | CPU DIMM 1 channel K temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_k_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU DIMM 1 channel K in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_k_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU DIMM 1 channel K in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_k_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU DIMM 1 channel K in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_l_temperature_celsius | Gauge | CPU DIMM 1 channel L temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_l_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU DIMM 1 channel L in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_l_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU DIMM 1 channel L in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_l_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU DIMM 1 channel L in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_m_temperature_celsius | Gauge | CPU DIMM 1 channel M temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_m_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU DIMM 1 channel M in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_m_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU DIMM 1 channel M in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_dimm_1_channel_m_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU DIMM 1 channel M in celsius | appliance, readingStatus |
| mqa_temperature_sensor_hardware_monitors_temperature_celsius | Gauge | Hardware monitors temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_hardware_monitors_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for hardware monitors in celsius | appliance, readingStatus |
| mqa_temperature_sensor_hardware_monitors_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for hardware monitors in celsius | appliance, readingStatus |
| mqa_temperature_sensor_hardware_monitors_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for hardware monitors in celsius | appliance, readingStatus |
| mqa_temperature_sensor_pch_temperature_celsius | Gauge | PCH temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_pch_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for PCH in celsius | appliance, readingStatus |
| mqa_temperature_sensor_pch_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for PCH in celsius | appliance, readingStatus |
| mqa_temperature_sensor_pch_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for PCH in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_1_hotspot_temperature_celsius | Gauge | Power supply 1 hotspot temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_1_hotspot_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for power supply 1 hotspot in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_1_hotspot_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for power supply 1 hotspot in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_1_hotspot_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for power supply 1 hotspot in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_2_hotspot_temperature_celsius | Gauge | Power supply 2 hotspot temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_2_hotspot_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for power supply 2 hotspot in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_2_hotspot_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for power supply 2 hotspot in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_2_hotspot_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for power supply 2 hotspot in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_1_intake_temperature_celsius | Gauge | Power supply 1 intake temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_1_intake_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for power supply 1 intake in celsius | appliance,  readingStatus |
| mqa_temperature_sensor_power_supply_1_intake_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for power supply 1 intake in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_1_intake_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for power supply 1 intake in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_2_intake_temperature_celsius | Gauge | Power supply 2 intake temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_2_intake_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for power supply 2 intake in celsius | appliance,  readingStatus |
| mqa_temperature_sensor_power_supply_2_intake_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for power supply 2 intake in celsius | appliance, readingStatus |
| mqa_temperature_sensor_power_supply_2_intake_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for power supply 2 intake in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_1_temperature_celsius | Gauge | CPU 1 temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_1_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU 1 in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_1_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU 1 in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_1_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU 1 in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_2_temperature_celsius | Gauge | CPU 2 temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_2_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for CPU 2 in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_2_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for CPU 2 in celsius | appliance, readingStatus |
| mqa_temperature_sensor_cpu_2_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for CPU 2 in celsius | appliance, readingStatus |
| mqa_temperature_sensor_inlet_1_temperature_celsius | Gauge | Inlet 1 temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_inlet_1_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for inlet 1 in celsius | appliance, readingStatus |
| mqa_temperature_sensor_inlet_1_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for inlet 1 in celsius | appliance, readingStatus |
| mqa_temperature_sensor_inlet_1_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for inlet 1 in celsius | appliance, readingStatus |
| mqa_temperature_sensor_outlet_1_temperature_celsius | Gauge | Outlet 1 temperature in celsius | appliance, readingStatus |
| mqa_temperature_sensor_outlet_1_upper_non_critical_threshold_temperature_celsius | Gauge | Upper non critical temperature threshold for outlet 1 in celsius | appliance, readingStatus |
| mqa_temperature_sensor_outlet_1_upper_critical_threshold_temperature_celsius | Gauge | Upper critical temperature threshold for outlet 1 in celsius | appliance, readingStatus |
| mqa_temperature_sensor_outlet_1_upper_non_recoverable_threshold_temperature_celsius | Gauge | Upper non recoverable temperature threshold for outlet 1 in celsius | appliance, readingStatus |

**Voltage Sensors**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_voltage_sensor_power_supply_1_in_voltage_volts | Gauge | Voltage going in power supply 1 in volts | appliance, readingStatus |
| mqa_voltage_sensor_power_supply_1_in_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of voltage going in power supply 1 in volts | appliance, readingStatus |
| mqa_voltage_sensor_power_supply_1_in_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of voltage going in power supply 1 in volts | appliance, readingStatus |
| mqa_voltage_sensor_power_supply_1_out_voltage_volts | Gauge | Voltage going out power supply 1 in volts | appliance, readingStatus |
| mqa_voltage_sensor_power_supply_1_out_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of voltage going out power supply 1 in volts | appliance, readingStatus |
| mqa_voltage_sensor_power_supply_1_out_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of voltage going out power supply 1 in volts | appliance, readingStatus |
| mqa_voltage_sensor_power_supply_2_in_voltage_volts | Gauge | Voltage going in power supply 2 in volts | appliance, readingStatus |
| mqa_voltage_sensor_power_supply_2_in_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of voltage going in power supply 2 in volts | appliance, readingStatus |
| mqa_voltage_sensor_power_supply_2_in_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of voltage going in power supply 2 in volts | appliance, readingStatus |
| mqa_voltage_sensor_power_supply_2_out_voltage_volts | Gauge | Voltage going out power supply 2 in volts | appliance, readingStatus |
| mqa_voltage_sensor_power_supply_2_out_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of voltage going out power supply 2 in volts | appliance, readingStatus |
| mqa_voltage_sensor_power_supply_2_out_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of voltage going out power supply 2 in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_15_volts | Gauge | Voltage +1.5 in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_15_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of +1.5 voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_15_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of +1.5 voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_18_volts | Gauge | Voltage +1.8 in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_18_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of +1.8 voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_18_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of +1.8 voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_12_volts | Gauge | Voltage +12 in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_12_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of +12 voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_12_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of +12 voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_33_volts | Gauge | Voltage +3.3 in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_33_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of +3.3 voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_33_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of +3.3 voltage +3.3 in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_5_volts | Gauge | Voltage +5 in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_5_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of +5 voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_5_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of +5 voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_5_standby_volts | Gauge | Voltage +5 standby in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_5_standby_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of +5 standby voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_5_standby_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of +5 standby voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_battery_volts | Gauge | Voltage battery in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_battery_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of battery voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_battery_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of battery voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_cpu_1_core_volts | Gauge | Voltage CPU 1 core in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_cpu_1_core_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of CPU 1 core voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_cpu_1_core_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of CPU 1 core voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_cpu_2_core_volts | Gauge | Voltage CPU 2 core in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_cpu_2_core_lower_critical_thereshold_voltage_volts | Gauge | Lower critical threshold of CPU 2 core voltage in volts | appliance, readingStatus |
| mqa_voltage_sensor_voltage_cpu_2_core_upper_critical_thereshold_voltage_volts | Gauge | Upper critical threshold of CPU 2 core voltage in volts | appliance, readingStatus |
