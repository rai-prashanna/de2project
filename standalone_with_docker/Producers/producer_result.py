import pulsar
from datetime import datetime, timedelta
import random
random.seed(datetime.now())
PULSAR_IP = 'pulsarbroker'
if __name__ == '__main__':
#Pulsar setup
    client = pulsar.Client('pulsar://' + PULSAR_IP + ':6650')
    producer = client.create_producer('DE2-result')
    #Craft update mesage
    msg = {}
    msg['type'] = 'Q1'
    language = {}
    language['Python'] = random.randint(500,1000)
    language['Java'] = random.randint(400,600)
    language['HTML'] = random.randint(200,400)
    language['C++'] = random.randint(100,200)
    language['Go'] = random.randint(0,100)
    language['JavaScript'] = random.randint(0,50)
    msg['result'] = language
    now = datetime.now().strftime("%Y/%m/%d,%H:%M:%S")
    msg['timestamp'] = now
    producer.send(str(msg).encode('utf-8'))
#Destroy pulsar client
    client.close()
