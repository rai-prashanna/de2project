import pulsar
import operator

if __name__ == '__main__':
    #Pulsar setup
    client = pulsar.Client('pulsar://localhost:6650')
    consumer = client.subscribe('DE2-Q1', subscription_name='DE-sub')
    #language list
    language = {}
    while True:
        msg = consumer.receive()
        try:
            content = msg.data().decode('utf-8')
            if content == 'end-here': #receive end signal
                #Sort language list in descending order of appearing times
                sorted_list = sorted(language.items(),key=operator.itemgetter(1),reverse=True)
                print("Analysis result: Top 10 most used programming language is")
                print(sorted_list[0:10])
                language = {}
            elif content in language.keys():
                language[content] += 1
            else:
                language[content] = 1
            consumer.acknowledge(msg)
        except:
            consumer.negative_acknowledge(msg)

    # Destroy pulsar client
    client.close()