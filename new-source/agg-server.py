import pulsar, _pulsar
import operator
import json
from datetime import datetime

PULSAR_IP = '192.168.2.139'

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

    while True:
        msg = consumer.receive()
        try:
            content = msg.data().decode('utf-8').replace("'", '"')
            update = json.loads(content)
            worker = update['worker']
            now = datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
            #Question 1
            if update['type'] == 'Q1':
                #Update to part list
                Q1_part['worker'] = update['result']
                #aggregate results
                Q1_final = agg_1(Q1_part)
                #Do smthing with the current updated result
                print("**********************************")
                print("[%s]Update >> Current result for Q1:" %now)
                print(Q1_final)
            #Question 2
            elif update['type'] == 'Q2':
                #Update to part list
                Q2_part['worker'] = update['result']
                #Aggregate results
                Q2_final = agg_2(Q2_part)
                print("**********************************")
                print("[%s]Update >> Current result for Q2:" %now)
                print(Q2_final)

            #Question 3
            elif update['type'] == 'Q3':
                #Update to part list
                Q3_part['worker'] = update['result']
                #aggregate results
                Q3_final = agg_1(Q3_part)
                #Do smthing with the current updated result
                print("**********************************")
                print("[%s]Update >> Current result for Q3:" %now)
                print(Q3_final)

            #Question 4
            elif update['type'] == 'Q4':
                #Update to part list
                Q4_part['worker'] = update['result']
                #aggregate results
                Q4_final = agg_1(Q4_part)
                #Do smthing with the current updated result
                print("**********************************")
                print("[%s]Update >> Current result for Q4:" %now)
                print(Q4_final)

            else:
                pass
            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)

    # Destroy pulsar client
    client.close()