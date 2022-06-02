import json
import pulsar, _pulsar
import operator
import sys
import json
from datetime import datetime

PULSAR_IP = 'pulsarbroker'

if __name__ == '__main__':

    #Pulsar setup
    client = pulsar.Client('pulsar://' + PULSAR_IP + ':6650')
    consumer = client.subscribe('DE2-repo', subscription_name='filter', consumer_type=_pulsar.ConsumerType.Shared)
    lang_producer = client.create_producer('DE2-lang')
    lang_producer_name = lang_producer.producer_name()
    commit_producer = client.create_producer('DE2-commit')
    commit_producer_name = commit_producer.producer_name()
    file_producer = client.create_producer('DE2-file')
    file_producer_name = file_producer.producer_name()

    recv_count = 0 #Number of received messages
    send_count = 0 #Number of sent messages
    error_count = 0 #Number of error messages <that could not be parsed in JSON format>
    #List of producers to the listening topic
    producer_list = []

    frequency = 100
    continue_flag = True
    while continue_flag:
        msg = consumer.receive()
        recv_count += 1
        now = datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
        try:
            content = msg.data().decode('utf-8').replace("'", '"').replace('None','"None"')
            producer_name = msg.properties()['producer']
            #Receive finish signal from producer
            if content == 'finish':
                if producer_name in producer_list:
                    print("[%s] A producer finished its requests: %s" %(now, producer_name))
                    producer_list.remove(producer_name) #Remove finished producer
                    #If no producer is working
                    if not producer_list:
                        continue_flag = False

            else:
                if producer_name not in producer_list:
                    print("[%s] New producer: %s" %(now, producer_name))
                    producer_list.append(producer_name)
                repo = json.loads(content)
                #If exist primary language
                if repo['primaryLanguage'] != "None":
                    #Extract language and send to language topic
                    repo_language = repo['primaryLanguage']['name']
                    lang_producer.send(repo_language.encode('utf-8'), properties={'producer': lang_producer_name})
                    send_count += 1

                    #Extract language/file list and craft message for file topic
                    file_msg = {}
                    file_msg['language'] = repo_language
                    file_msg['file_list'] = repo['object']['entries']
                    file_producer.send(str(file_msg).encode('utf-8'), properties={'producer': file_producer_name})
                    send_count += 1

                #Extract name/commit count list and craft message for commit topic
                commit_msg = {}
                commit_msg['name'] = repo['nameWithOwner']
                commit_msg['commit_count'] = repo['refs']['nodes']
                commit_producer.send(str(commit_msg).encode('utf-8'), properties={'producer': commit_producer_name})
                send_count += 1

                if recv_count % frequency == 1:
                    print("[%s] Total messages>>Received: %d, Error Reading: %d, Sent: %d" %(now, recv_count, error_count, send_count))
            consumer.acknowledge(msg)
        except Exception as e:
            error_count += 1
            consumer.acknowledge(msg)

    print("-----------------------------------------")
    print("Finished filtering all repositories!!")
    print("Total messages>>Received: %d, Error Reading: %d, Sent: %d" %(recv_count, error_count, send_count))
    #Send finish signal
    lang_producer.send("finish".encode('utf-8'), properties={'producer': lang_producer_name})
    commit_producer.send("finish".encode('utf-8'), properties={'producer': commit_producer_name})
    file_producer.send("finish".encode('utf-8'), properties={'producer': file_producer_name})
    # Destroy pulsar client
    lang_producer.close()
    commit_producer.close()
    file_producer.close()
    client.close()
