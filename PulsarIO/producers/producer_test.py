import pulsar
from datetime import datetime, timedelta
import random
random.seed(datetime.now())
​
PULSAR_IP = 'localhost' 
​
if __name__ == '__main__':
​
    #Pulsar setup
    client = pulsar.Client('pulsar://' + PULSAR_IP + ':6650')
    producer = client.create_producer('DE2-pulsario')
    
    #Craft update mesage
    msg = {}
    msg['type'] = 'Q1'
    language = {}
    language['Python'] = random.randint(0,300)
    language['Java'] = random.randint(0,300)
    language['HTML'] = random.randint(0,300)
    language['RUST'] = random.randint(0,300)
    language['WTF'] = random.randint(0,300)
    language['TESTING'] = random.randint(0,300)
​
    msg['result'] = language
​
    producer.send(str(msg).encode('utf-8'))
​
    #Destroy pulsar client
    client.close()