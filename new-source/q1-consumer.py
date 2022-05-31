import pulsar, _pulsar
import operator
import sys
import socket
from datetime import datetime

PULSAR_IP = '192.168.2.139'

if __name__ == '__main__':
    #Pulsar setup
    client = pulsar.Client('pulsar://' + PULSAR_IP + ':6650')
    consumer = client.subscribe('DE2-lang', subscription_name='DE-Q1', consumer_type=_pulsar.ConsumerType.Shared)
    agg_producer = client.create_producer('DE2-agg')
    #language list
    language = {}
    #Aggregation message
    agg_msg = {}
    agg_msg['type'] = 'Q1'
    msg_count = 0
    frequency = 100 #frequency of printing top list/send update

    while True:
        msg = consumer.receive()
        msg_count += 1
        try:
            content = msg.data().decode('utf-8')
            now = datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
            if content in language.keys():
                language[content] += 1
            else:
                language[content] = 1
            #Periodically print out list of languages and project counts
            if msg_count % frequency == 1:
                print("[%s] Current list of language count from %d messages:" %(now,msg_count))
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