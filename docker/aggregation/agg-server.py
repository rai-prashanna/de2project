import pulsar, _pulsar
import operator
import json
from datetime import datetime

PULSAR_IP = 'pulsarbroker'

#aggregation function for Q1 Q3 Q4
def agg_1(part: dict):
    final = {}
    #Iterate result of each worker
    for worker, result in part.items():
        for language, count in result.items():
            if language in final.keys():
                final[language] += count
            else:
                final[language] = count
    return dict(sorted(final.items(), key=operator.itemgetter(1), reverse=True)[0:10])

#aggregation function for Q2
def agg_2(part: dict):
    final = {}
    #Iterate result of each worker and merge to the final result
    for worker, result in part.items():
        final.update(result)
    #Sort result and return top 10
    return dict(sorted(final.items(), key=operator.itemgetter(1), reverse=True)[0:10])

if __name__ == '__main__':
    #Pulsar setup
    client = pulsar.Client('pulsar://' + PULSAR_IP + ':6650')
    consumer = client.subscribe('DE2-agg', subscription_name='DE-agg', consumer_type=_pulsar.ConsumerType.Exclusive)
    producer = client.create_producer('DE2-result')    
    ##List of producers to the listening topic
    producer_list = []
    #Q1 list:
    Q1_part = {}
    Q1_final = {}
    #Q2 list:
    Q2_part = {}
    Q2_final = {}
    #Q3 list:
    Q3_part = {}
    Q3_final = {}
    #Q4 list:
    Q4_part = {}
    Q4_final = {}

    update_msg = {}

    start_time = None

    continue_flag = True
    while continue_flag:
        msg = consumer.receive()
        now = datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
        try:
            producer_name = msg.properties()['producer']
            content = msg.data().decode('utf-8').replace("'", '"')
            #Receive start signal from request-producer
            if content == 'start':
                if start_time == None:
                    start_time = datetime.now()
                    print("[%s] Program starts!!!" %start_time)
            
            #Receive finish signal from producer
            elif content == 'finish':
                if producer_name in producer_list:
                    print("[%s] A producer finished its job: %s" %(now, producer_name))
                    producer_list.remove(producer_name) #Remove finished producer
                    #If no producer is working
                    if not producer_list:
                        continue_flag = False
            else:
                if producer_name not in producer_list:
                    print("[%s] New producer: %s" %(now, producer_name))
                    producer_list.append(producer_name)
                update = json.loads(content)
                update_msg['type'] = update['type']
                update_msg['timestamp'] = now
                #Question 1
                if update['type'] == 'Q1':
                    #Update to part list
                    Q1_part[producer_name] = update['result']
                    #aggregate results
                    Q1_final = agg_1(Q1_part)
                    #Do smthing with the current updated result
                    print("**********************************")
                    print("[%s]Update >> Current result for Q1:" %now)
                    print(Q1_final)
                    update_msg['result'] = Q1_final
                #Question 2
                elif update['type'] == 'Q2':
                    #Update to part list
                    Q2_part[producer_name] = update['result']
                    #Aggregate results
                    Q2_final = agg_2(Q2_part)
                    print("**********************************")
                    print("[%s]Update >> Current result for Q2:" %now)
                    print(Q2_final)
                    update_msg['result'] = Q2_final
                #Question 3
                elif update['type'] == 'Q3':
                    #Update to part list
                    Q3_part[producer_name] = update['result']
                    #aggregate results
                    Q3_final = agg_1(Q3_part)
                    #Do smthing with the current updated result
                    print("**********************************")
                    print("[%s]Update >> Current result for Q3:" %now)
                    print(Q3_final)
                    update_msg['result'] = Q3_final
                #Question 4
                elif update['type'] == 'Q4':
                    #Update to part list
                    Q4_part[producer_name] = update['result']
                    #aggregate results
                    Q4_final = agg_1(Q4_part)
                    #Do smthing with the current updated result
                    print("**********************************")
                    print("[%s]Update >> Current result for Q4:" %now)
                    print(Q4_final)
                    update_msg['result'] = Q4_final
                
                #Send to final topic for pulsarIO
            producer.send(str(update_msg).encode('utf-8'))
                
            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)

    print("Final result acquired!")
    print("--------------Q1--------------")
    print(Q1_final)
    print("--------------Q2--------------")
    print(Q2_final)
    print("--------------Q3--------------")
    print(Q3_final)
    print("--------------Q4--------------")
    print(Q4_final)
    print("------------------------------")
    #print("Total amount of processing time: ", (datetime.now() - start_time).seconds ," seconds")
    
    # Destroy pulsar client
    producer.close()
    consumer.close()
    client.close()