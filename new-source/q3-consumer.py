import pulsar, _pulsar
import re
import json
import socket
from datetime import datetime

PULSAR_IP = '192.168.2.139'

keywords = ['test', 'spec']
regex_expression = '(\s|^|\W|\d)' + "|".join(map(re.escape, keywords)) + '(\s|$|\W|\d)'

def has_unit_test(list = list):
    for unit in list:
        #search for pattern in its name
        if re.search(regex_expression, unit['name'], re.IGNORECASE):
            return 1
        #If being directory -> search inside
        if unit['type'] == "tree":
            sub_dir = unit['object']['entries']
            for sub_unit in sub_dir:
                if re.search(regex_expression, sub_unit['name'], re.IGNORECASE):
                    return 1
    return 0

if __name__ == '__main__':
    #Pulsar setup
    client = pulsar.Client('pulsar://' + PULSAR_IP + ':6650')
    consumer = client.subscribe('DE2-file', subscription_name='DE-Q3', consumer_type=_pulsar.ConsumerType.Shared)
    agg_producer = client.create_producer('DE2-agg')
    #language list
    language = {}
    #Aggregation message
    agg_msg = {}
    agg_msg['type'] = 'Q3'

    msg_count = 0
    frequency = 100 #frequency of printing top list/send update

    while True:
        msg = consumer.receive()
        msg_count += 1
        try:
            now = datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
            content = msg.data().decode('utf-8').replace("'", '"')
            repo = json.loads(content)
            repo_language = repo['language']
            file_list = repo['file_list']
            if has_unit_test(file_list):
                if repo_language in language.keys():
                    language[repo_language] += 1
                else:
                    language[repo_language] = 1
            #Periodically print out list of languages and project counts
            if msg_count % frequency == 1:
                print("[%s]Current list of language count for repositories with unit-test from %d messages:" %(now, msg_count))
                print(language)
                #Craft message to the aggregation server
                agg_msg['worker'] = socket.gethostname() #for agg server tell apart different replicas of a consumer
                agg_msg['result'] = language
                #Send aggregation message
                agg_producer.send(str(agg_msg).encode('utf-8'))
                
            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)

    # Destroy pulsar client
    client.close()