import pulsar, _pulsar
import operator
import sys

if __name__ == '__main__':
    #Pulsar setup
    client = pulsar.Client('pulsar://localhost:6650')
    consumer = client.subscribe('DE2-lang', subscription_name='DE-Q1', consumer_type=_pulsar.ConsumerType.Shared)
    #language list
    language = {}
    count = 0
    frequency = 10 #frequency of printing top list/send update

    while True:
        msg = consumer.receive()
        try:
            content = msg.data().decode('utf-8')
            if content in language.keys():
                language[content] += 1
            else:
                language[content] = 1
            count += 1
            #Periodically print out list of languages and project counts
            if count == frequency:
                print("Current list of language count:")
                print(language)
                count = 0
            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)

    # Destroy pulsar client
    client.close()