import json
import pulsar, _pulsar
import operator
import sys
import json

if __name__ == '__main__':

    #Pulsar setup
    client = pulsar.Client('pulsar://192.168.2.139:6650')
    consumer = client.subscribe('DE2-repo', subscription_name='filter', consumer_type=_pulsar.ConsumerType.Shared)
    lang_producer = client.create_producer('DE2-lang')
    commit_producer = client.create_producer('DE2-commit')
    file_producer = client.create_producer('DE2-file')
    recv_count = 0
    send_count = 0
    
    frequency = 100
    while True:
        msg = consumer.receive()
        recv_count += 1
        try:
            content = msg.data().decode('utf-8')
            repo = json.loads(content)

            # #Extract language and send to language topic
            repo_language = repo['primaryLanguage']['name']
            lang_producer.send(repo_language.encode('utf-8'))
            send_count += 1

            #Extract name/commit count list and craft message for commit topic
            commit_msg = {}
            commit_msg['name'] = repo['nameWithOwner']
            commit_msg['commit_count'] = repo['refs']['nodes']
            commit_producer.send(str(commit_msg).encode('utf-8'))
            send_count += 1

            #Extract language/file list and craft message for file topic
            file_msg = {}
            file_msg['language'] = repo_language
            file_msg['file_list'] = repo['object']['entries']
            file_producer.send(str(file_msg).encode('utf-8'))
            send_count += 1

            if recv_count % frequency == 1:
                print("Total messages>>Received: %d, Sent: %d" %(recv_count, send_count))
            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)

    # Destroy pulsar client
    client.close()
    lang_producer.close()
    commit_producer.close()
    file_producer.close()