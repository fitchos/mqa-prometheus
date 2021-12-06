FROM python:3.6
USER root

RUN pip install prometheus-client
RUN pip install requests

ENV EXPORTER_APPLIANCE_NAME="MQ_APPLIANCE_NAME" \
    EXPORTER_APPLIANCE_IP="localhost" \
    EXPORTER_APPLIANCE_REST_PORT=5554 \
    EXPORTER_APPLIANCE_USER=admin \
    EXPORTER_APPLIANCE_PASSWORD=mypassword \
    EXPORTER_REST_PORT=7070 \
    EXPORTER_REST_LOG_FILE=/home/exporter/log/mylog_file.log


COPY ./code /home/exporter/src
RUN mkdir /home/exporter/log
WORKDIR /home/exporter

ENTRYPOINT python /home/exporter/src/mqa_metrics.py \
    -a $EXPORTER_APPLIANCE_NAME \
    -i $EXPORTER_APPLIANCE_IP \
    -p $EXPORTER_APPLIANCE_REST_PORT \
    -u $EXPORTER_APPLIANCE_USER \
    -x $EXPORTER_APPLIANCE_PASSWORD \
    -hp $EXPORTER_REST_PORT \
    -l $EXPORTER_REST_LOG_FILE