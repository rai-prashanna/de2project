import pulsar, _pulsar
from datetime import datetime
import time

PULSAR_IP = 'pulsarbroker'

if __name__ == '__main__':
    #Pulsar setup
    client = pulsar.Client('pulsar://' + PULSAR_IP + ':6650')
    consumer = client.subscribe('DE2-lang', subscription_name='DE-Q1', consumer_type=_pulsar.ConsumerType.Shared)
    agg_producer = client.create_producer('DE2-agg')
    agg_producer_name = agg_producer.producer_name()
    #language list
    language = {}
    ##List of producers to the listening topic
    producer_list = []
    #Aggregation message
    agg_msg = {}
    agg_msg['type'] = 'Q1'
    msg_count = 0
    frequency = 100 #frequency of printing top list/send update

    continue_flag = True
    while continue_flag:
        msg = consumer.receive()
        msg_count += 1
        now = datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
        try:
            producer_name = msg.properties()['producer']
            content = msg.data().decode('utf-8')
            #Receive finish signal from producer
            if content == 'finish':
                if producer_name in producer_list:
                    print("[%s] A producer finished its job: %s" %(now, producer_name))
                    producer_list.remove(producer_name) #Remove finished producer
                    #If no producer is working
                    if not producer_list:
                        agg_msg['result'] = language
                        #Update the latest result to the aggregation server
                        agg_producer.send(str(agg_msg).encode('utf-8'), properties={'producer': agg_producer_name})
                        continue_flag = False
            else:
                if producer_name not in producer_list:
                    print("[%s] New producer: %s" %(now, producer_name))
                    producer_list.append(producer_name)
                
                if content in language.keys():
                    language[content] += 1
                else:
                    language[content] = 1
                #Periodically print out list of languages and project counts
                if msg_count % frequency == 1:
                    print("[%s] Current list of language count from %d messages:" %(now,msg_count))
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