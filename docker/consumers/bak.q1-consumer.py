import pulsar
import operator
import sys
import time

if __name__ == '__main__':
    #Validate program arguments
    args = sys.argv[1:]
    if len(args) != 1:
        print("Program requires 1 input arg: number of top repos")
        sys.exit(1)
    n_repos = args[0]
    #Pulsar setup
    client = pulsar.Client('pulsar://pulsarbroker:6650')
    
    #consumer = client.subscribe("Q1", subscription_name="Q1")
    def my_listener(consumer, msg):
    # process message
        print("my_listener read message '%s' id='%s'", msg.data().decode('utf-8'), msg.message_id())
        consumer.acknowledge(msg)

    consumer = client.subscribe('Q1', 'my-subscription',consumer_type=pulsar.ConsumerType.Exclusive,initial_position=pulsar.InitialPosition.Latest,message_listener=my_listener,negative_ack_redelivery_delay_ms=60000) 
    #language list
    language = {}
    # while True:
    #     msg = consumer.receive()
    #     try:
    #         content = msg.data().decode('utf-8')
    #         consumer.acknowledge(msg)
    #         if content == 'end-here': #receive end signal
    #             #Sort language list in descending order of appearing times
    #             sorted_list = sorted(language.items(),key=operator.itemgetter(1),reverse=True)
    #             print("Analysis result: Top %s most used programming languages are" %n_repos)
    #             print(sorted_list[0:int(n_repos)])
    #             language = {}
    #         elif content in language.keys():
    #             language[content] += 1
    #         else:
    #             language[content] = 1
            
    #     except:
    #         consumer.negative_acknowledge(msg)
    time.sleep(100)

    # Destroy pulsar client
    client.close()
