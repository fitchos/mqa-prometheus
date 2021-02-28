# mqa-prometheus
This project provides a Prometheus Exporter for the IBM MQ Appliance. 

![IBM MQ Appliance](/images/IBM_MQ_Appliance.png)

## WARNING
The main branch is the development branch which may not be stable!

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
You must run a separate exporter for each MQ Appliance you want to collect metrics for.

mqa_metrics.py is the name of the module to run an exporter. Only basic authentication is
currently supported.

**Note: if you use Python 2 and log to a file, you need to use an external mechanism to rotate the logs**

```
Usage: mqa_metrics.py [-h] -a APPLIANCE -i IP [-hp HTTPPORT] [-l LOG] [-ln LOGNUMBERS] [-ls LOGSIZE] -p PORT
                      [-t TIMEOUT] -u USER [-x PW]

MQ Appliance Prometheus Exporter - vx.x

optional arguments:
  -h, --help            show this help message and exit
  -a APPLIANCE, --appliance APPLIANCE
                        Name of the appliance
  -i IP, --ip IP        IP address of the appliance REST API
  -hp HTTPPORT, --httpPort HTTPPORT
                        Port number of the exported HTTP server (default: 8000)
  -l LOG, --log LOG     Name of the log file (defaults to STDOUT)
  -ln LOGNUMBERS, --lognumbers LOGNUMBERS
                        Number of logs in a rotation (defaults to 10)
  -ls LOGSIZE, --logsize LOGSIZE
                        Size of logs in bytes (defaults to 10MB - 10485760)
  -p PORT, --port PORT  Port number of the appliance REST API
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in seconds to perform the REST API call (default: 15)
  -u USER, --user USER  User to login to the appliance
  -x PW, --pw PW        Password to login to the appliance
```

### Sample commands to run an exporter
Run an exporter with logging output to STDOUT and password being prompted on the command line

```
mqa_metrics.py -a MQAPROD1 -i 192.168.28.250 -p 5554 -u admin -hp 8000
```

Run an exporter with logging output to a file using all logging defaults

```
mqa_metrics.py -a MQAPROD1 -i 192.168.28.250 -p 5554 -u admin -x mypassword -hp 8000 -l mqaprod1.log 
```

Run a second exporter (note: the HTTPPORT must be different)

```
mqa_metrics.py -a MQAPROD2 -i 192.168.28.210 -p 5554 -u admin -x mypassword -hp 8001 -l mqaprod2.log
```

### Utilities to manage exporters
Three utilities are available to:

1. Start multiple exporters using a CSV file
2. List the exporters currently running
3. Stop one or more exporters

**Note: Environment variable MQA_EXPORTER_DIRECTORY can be set to a directory name**
      **and avoid having to specify the -d parameter on the commands**

#### Starting multiple exporters
To start multiple exporters build a CSV (comma delimited) file with the following information:

- appliance name
- IP or DNS name of the appliance
- Port number of the REST API
- Port number to serve the metrics to Prometheus
- Timeout value for the REST API calls to the appliance

To start the exporters, use the mqa_start_exporters utility

```
Usage: mqa_start_exporters.py [-h] [-d DIRECTORY] -f FILE [-ln LOGNUMBERS] [-ls LOGSIZE] -u USER [-x PW]

MQ Appliance Prometheus Exporter Start Utility - vx.x

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Path to directory for log and PID files (defaults to current directory
  -f FILE, --file FILE  Name of the file with the exporters configuration (CSV)
  -ln LOGNUMBERS, --lognumbers LOGNUMBERS
                        Number of logs in a rotation (defaults to 10)
  -ls LOGSIZE, --logsize LOGSIZE
                        Size of logs in bytes (defaults to 10MB - 10485760)
  -u USER, --user USER  User to login to the appliance
  -x PW, --pw PW        Password to login to the appliance
```

#### Sample command to start a list of exporters
```
mqa_start_exporters.py -f my_exporter_list.csv -d \temp -u admin 
```

#### Listing exporters currently running
To list the exporters currently running, use the mqa_list_exporters utility

```
Usage: mqa_list_exporters.py [-h] [-a APPLIANCE] [-d DIRECTORY]

MQ Appliance Prometheus Exporter List Utility - v0.3

optional arguments:
  -h, --help            show this help message and exit
  -a APPLIANCE, --appliance APPLIANCE
                        Name of the appliance
  -d DIRECTORY, --directory DIRECTORY
                        Path to directory for PID files (defaults to current directory)
```

#### Sample commands to list exporters running
```
mqa_list_exporters.py -d \temp
mqa_list_exporters.py -d \temp -a my_appliance
```

#### Stopping one or more exporters
To stop one or more exporters, use the mqa_stop_exporters utility

```
usage: mqa_stop_exporters.py [-h] [-a APPLIANCE] [-d DIRECTORY]

MQ Appliance Prometheus Exporter Stop Utility - v0.3

optional arguments:
  -h, --help            show this help message and exit
  -a APPLIANCE, --appliance APPLIANCE
                        Name of the appliance
  -d DIRECTORY, --directory DIRECTORY
                        Path to directory for PID files (defaults to current directory)
```

#### Sample commands to stop one or more exporters
```
mqa_stop_exporters.py -d \temp
mqa_list_exporters.py -d \temp -a my_appliance
```

### Available metrics
**Active Users**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_active_users_total | Gauge | Total active users connected to the appliance | appliance, connection |

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

**File System**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_file_system_encrypted_bytes_free | Gauge | Free, or unused and available, encrypted storage space on the appliance | appliance |
| mqa_file_system_encrypted_bytes_total | Counter | Total encrypted storage space on the appliance (the maximum capacity) | appliance |
| mqa_file_system_temporary_bytes_free | Gauge | Free, or unused and available, temporary storage space on the appliance | appliance |
| mqa_file_system_temporary_bytes_total | Counter | Total temporary storage space on the appliance | appliance |
| mqa_file_system_internal_bytes_free | Gauge | Free, or unused and available, internal storage space on the appliance | appliance |
| mqa_file_system_internal_bytes_total | Counter | Total internal storage space on the appliance | appliance |

**Log Targets**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_log_target_events_processed_total | Counter | The number of events that this log target processed | appliance, name |
| mqa_log_target_events_dropped_total | Counter | The number of events that this log target dropped because there are too many pending events | appliance, name |
| mqa_log_target_events_pending_total | Counter | The number of pending events for this log target. These events are waiting to be stored at the destination | appliance, name |

**Log Targets Information**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_log_target_info | Info | MQ Appliance log target information | appliance, name, status, errorInfo, eventsProcessed, eventsDropped, eventsPending,requestedMemory |

**MQ Appliance Information**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_info | Info | MQ Appliance information | appliance, bootcount, bootuptime, build, builddate, deliverytype, installdate, installeddpos, level, machinetype, modeltype, runningdpos, serial, time, timezone, type, tzspec, uptime, version, watchdogbuild, xmlaccelerator |

**MQ Resources**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_mq_resources_storage_bytes_total | Counter | The total storage in bytes available for IBM MQ data | appliance |
| mqa_mq_resources_storage_bytes_used | Gauge | The amount of IBM MQ storage in use in bytes | appliance |
| mqa_mq_resources_errors_storage_bytes_total | Counter | The total storage in bytes available for IBM MQ error logs | appliance |
| mqa_mq_resources_errors_storage_bytes_used | Gauge | The amount of IBM MQ error log storage in use in bytes | appliance |
| mqa_mq_resources_trace_storage_bytes_total | Counter | The total storage in bytes available for IBM MQ trace | appliance |
| mqa_mq_resources_trace_storage_bytes_used | Gauge | The amount of IBM MQ trace storage in bytes in use | appliance |

**Network Interface**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_network_interface_rx_bytes_total | Counter | The amount of data successfully received on the interface, which includes MAC framing overhead | appliance, adminStatus, name, operStatus |
| mqa_network_interface_rx_packets_total | Counter | The number of packets successfully received on the interface that were passed up to the network layer for processing | appliance, adminStatus, name, operStatus |
| mqa_network_interface_rx_errors_total | Counter | The number of packets that could not be received due to errors in the packet or in the hardware | appliance, adminStatus, name, operStatus |
| mqa_network_interface_rx_drops_total | Counter | The number of received packets that were not in error, but were not passed up to the network layer due to resource constraints | appliance, adminStatus, name, operStatus |
| mqa_network_interface_tx_bytes_total | Counter | The amount of data successfully transmitted on the interface, which includes MAC framing overhead | appliance, adminStatus, name, operStatus |
| mqa_network_interface_tx_packets_total | Counter | The number of packets successfully transmitted on the interface | appliance, adminStatus, name, operStatus |
| mqa_network_interface_tx_errors_total | Counter | The number of packets that were not successfully transmitted due to errors on the network or in the hardware | appliance, adminStatus, name, operStatus |
| mqa_network_interface_tx_drops_total | Counter | The number of packets that were not transmitted because the network layer was generating packets faster than the physical network could accept them | appliance, adminStatus, name, operStatus |

**Network Interface Information**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_network_interface_info | Info | MQ Appliance network interface information | appliance, interfaceIndex, interfaceType, name, adminStatus, operStatus, ipType, ip, prefixLength, macAddress, mtu |

**Queue Manager**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_queue_manager_cpu_usage | Gauge | The instantaneous CPU usage by the queue manager as a percentage of the CPU load | appliance, qm |
| mqa_queue_manager_memory_bytes_used | Gauge | The amount of memory in bytes that is currently in use by the queue manager | appliance, qm |
| mqa_queue_manager_fs_bytes_used | Gauge | The amount of file system in bytes that is currently in use by the queue manager | appliance, qm |
| mqa_queue_manager_fs_bytes_allocated | Gauge | The amount of file system in bytes allocated for the queue manager | appliance, qm |

**Queue Manager Information**
| Metric | Type | Description | Labels |
|------------------------|-------| ----------------------------------------------| ----------------------|
| mqa_queue_manager_info | Info | MQ Appliance queue manager information | appliance, qm, status, haRole, haStatus, drRole, drStatus |

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

**TCP Connections**
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

