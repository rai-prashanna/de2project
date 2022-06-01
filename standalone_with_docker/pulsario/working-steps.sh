

/pulsar/bin/pulsar-admin sink create --sink-type mongo --sink-config-file /home/mongodb-sink.yml --inputs test-mongo

/pulsar/bin/pulsar-client produce -m "{firstname: \"P\", lastname: \"RAI\"}" -s % -n 10 test-mongo


/pulsar/bin/pulsar-admin sink available-sinks
/pulsar/bin/pulsar-admin sink list
/pulsar/bin/pulsar-admin sink status --name mongo-test-sink

**********
use pulsar_in_action;
db.example.save({ firstname: "John", lastname: "Smith"})
