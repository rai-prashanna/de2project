import pulsar, _pulsar
import re
import json
from datetime import datetime
import time

PULSAR_IP = '192.168.2.139'

unit_test_keywords = ['test', 'spec']
unit_test_regex = '(\s|^|\W|\d)' + "|".join(map(re.escape, unit_test_keywords)) + '(\s|$|\W|\d)'

cicd_keywords = ['cicd', '.gitlab-ci.yml', '.travis', '.circleci', 'Jenkinsfile' ]
cicd_regex = '(\s|^|\W|\d)' + "|".join(map(re.escape, cicd_keywords)) + '(\s|$|\W|\d)'

def has_unit_test(list = list):
    for unit in list:
        #search for pattern in its name
        if re.search(unit_test_regex, unit['name'], re.IGNORECASE):
            return 1
        #If being directory -> search inside
        if unit['type'] == "tree":
            sub_dir = unit['object']['entries']
            for sub_unit in sub_dir:
                if re.search(unit_test_regex, sub_unit['name'], re.IGNORECASE):
                    return 1
                if unit['name'] == '.github' and sub_unit['name'] == 'workflows':
                    return 1
    return 0


def has_cicd(list = list):
    for unit in list:
        #search for pattern in its name
        if re.search(cicd_regex, unit['name'], re.IGNORECASE):
            return 1
        #If being directory -> search inside
        if unit['type'] == "tree":
            sub_dir = unit['object']['entries']
            for sub_unit in sub_dir:
                if re.search(cicd_regex, sub_unit['name'], re.IGNORECASE):
                    return 1
                if unit['name'] == '.github' and sub_unit['name'] == 'workflows':
                    return 1
    return 0

if __name__ == '__main__':
    #Pulsar setup
    client = pulsar.Client('pulsar://' + PULSAR_IP + ':6650')
    consumer = client.subscribe('DE2-file', subscription_name='DE-Q4', consumer_type=_pulsar.ConsumerType.Shared)
    agg_producer = client.create_producer('DE2-agg')
    agg_producer_name = agg_producer.producer_name()
    #language list
    language = {}
    #List of producers to the listening topic
    producer_list = []
    #Aggregation message
    agg_msg = {}
    agg_msg['type'] = 'Q4'

    msg_count = 0
    frequency = 100 #frequency of printing top list/send update

    continue_flag = True
    while continue_flag:
        msg = consumer.receive()
        now = datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
        msg_count += 1
        try:
            producer_name = msg.properties()['producer']
            content = msg.data().decode('utf-8').replace("'", '"')
            #Receive finish signal from producer
            if content == 'finish':
                if producer_name in producer_list:
                    print("[%s] A producer finished its job: %s" %(now, producer_name))
                    producer_list.remove(producer_name) #Remove finished producer
                    #If no producer is working
                    if not producer_list:
                        agg_msg['result'] = language
                        #Update last time
                        agg_producer.send(str(agg_msg).encode('utf-8'), properties={'producer': agg_producer_name})
                        continue_flag = False
            else:
                if producer_name not in producer_list:
                    print("[%s] New producer: %s" %(now, producer_name))
                    producer_list.append(producer_name)
                
                repo = json.loads(content)
                repo_language = repo['language']
                file_list = repo['file_list']
                if has_unit_test(file_list) and has_cicd(file_list):
                    if repo_language in language.keys():
                        language[repo_language] += 1
                    else:
                        language[repo_language] = 1
                #Periodically print out list of languages and project counts
                if msg_count % frequency == 1:
                    print("[%s]Current list of language count for repositories with unit-test from %d messages:" %(now, msg_count))
                    print(language, "\n")
                    #Craft message to the aggregation server
                    agg_msg['result'] = language
                    #Send aggregation message
                    agg_producer.send(str(agg_msg).encode('utf-8'), properties={'producer': agg_producer_name})
                
            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)

    time.sleep(1)
    #Send ending signal to aggregation server
    agg_producer.send("finish".encode('utf-8'), properties={'producer': agg_producer_name})
    print("Fisnished all available jobs! Quitting...")
    # Destroy pulsar client
    agg_producer.close()
    client.close()