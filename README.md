# mqa-prometheus
This project provide a Prometheus Exporter for the IBM MQ Appliance. 

## Prerequisites
The following are prerequisites to run the exporter:
1. Prometheus (https://prometheus.io/download/)
2. Python 3.x (https://www.python.org/downloads/)
3. Prometheus Python client library
    ```
      pip install prometheus-client
    ```
4. Python Requests library
    ```
      pip install requests
    ```
5. MQ Appliance REST API must be enabled

## Getting Started
You must run a separate exporter for each MQ Appliance you want to collect metrics for.

mqa_metrics.py is the name of the module to run an exporter

```
Usage: mqa_metrics.py [-h] -a APPLIANCE -i IP [-hp HTTPPORT] [-l LOG] [-ln LOGNUMBERS] [-ls LOGSIZE] -p PORT
                      [-t TIMEOUT] -u USER [-x PW]

MQ Appliance Prometheus Exporter

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
    mqa_metrics.py -a MQA2002PROD1 -i 192.168.28.250 -p 5554 -u admin -hp 8000
    ```

Run an exporter with logging output to a file using all logging defaults
    ```
    mqa_metrics.py -a MQA2002PROD1 -i 192.168.28.250 -p 5554 -u admin -x mypassword -hp 8000 -l mqa2002prod1.log 
    ```
    
Run a second exporter (note: the HTTPPORT must be different)
    ```
    mqa_metrics.py -a MQA2002PROD2 -i 192.168.28.210 -p 5554 -u admin -x mypassword -hp 8001 -l mqa2002prod2.log
    ```
