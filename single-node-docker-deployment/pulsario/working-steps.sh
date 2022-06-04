docker exec pulsarbroker /pulsar/bin/pulsar-admin sink create --sink-type mongo --sink-config-file /home/mongodb-sink.yml --inputs DE2-agg

docker exec 89b5aeaadd1b /pulsar/bin/pulsar-admin sink create --sink-type mongo --sink-config-file /home/mongodb-sink.yml --inputs DE2-result

/pulsar/bin/pulsar-client produce -m "{firstname: \"P\", lastname: \"RAI\"}" -s % -n 10 test-mongo


/pulsar/bin/pulsar-admin sink available-sinks
/pulsar/bin/pulsar-admin sink list
/pulsar/bin/pulsar-admin sink status --name mongo-test-sink

**********
use pulsar_in_action;
db.example.save({ firstname: "John", lastname: "Smith"})


.travis
.github/workflows
Jenkinsfile <it is file not directory located into project directory>
.circleci