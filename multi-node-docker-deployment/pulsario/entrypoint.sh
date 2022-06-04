#!/bin/sh
echo "start pulsar in background......."
cd /home
nohup /pulsar/bin/pulsar standalone &
sleep 100
/pulsar/bin/pulsar-admin sink create --sink-type mongo --sink-config-file /home/mongodb-sink.yml --inputs test-mongo




