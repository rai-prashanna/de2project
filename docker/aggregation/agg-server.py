import pulsar, _pulsar
import operator
import json

#aggregation function for Q1 Q3 Q4
def agg_1(part: dict):
    final = {}
    #Iterate result of each worker
    for worker, result in part.items():
        for language, count in result.items():
            if language in final.keys():
                final['language'] += count
            else:
                final['language'] = count
    return final

#aggregation function for Q2
def agg_2(part: dict):
    temp = {}
    #Iterate result of each worker
    for result in part:
        temp.update(result)
    #Sort result
    sorted = sorted(temp.items(),key=operator.itemgetter(1),reverse=True)
    return sorted[0:10]

if __name__ == '__main__':
    #Pulsar setup
    client = pulsar.Client('pulsar://localhost:6650')
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
            #Question 1
            if update['type'] == 'Q1':
                #Update to part list
                Q1_part['worker'] = worker['result']
                #aggregate results
                Q1_final = agg_1(Q1_part)
                #Do smthing with the current updated result
                print("Current result for Q1:")
                print(Q1_final)
            #Question 2
            elif update['type'] == 'Q2':
                #Update to part list
                Q2_part['worker'] = worker['result']
                #Aggregate results
                Q2_final = agg_2(Q2_part)
                print("Current result for Q2:")
                print(Q2_final)

            #Question 3
            elif update['type'] == 'Q3':
                #Update to part list
                Q3_part['worker'] = worker['result']
                #aggregate results
                Q3_final = agg_1(Q3_part)
                #Do smthing with the current updated result
                print("Current result for Q3:")
                print(Q3_final)
            
            #Question 4
            elif update['type'] == 'Q4':
                #Update to part list
                Q4_part['worker'] = worker['result']
                #aggregate results
                Q4_final = agg_1(Q4_part)
                #Do smthing with the current updated result
                print("Current result for Q3:")
                print(Q4_final)
            else:
                pass
            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)

    # Destroy pulsar client
    client.close()