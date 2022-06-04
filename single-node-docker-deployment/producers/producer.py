#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#


#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import pulsar

if __name__ == '__main__':
    pass

client = pulsar.Client('pulsar://pulsarbroker:6650')   

producer = client.create_producer('my-topic',producer_name='my-python-producer',
   block_if_queue_full=True,
   batching_enabled=True,
   batching_max_publish_delay_ms=10)    

for i in range(10):
    producer.send(
        ('Hello-%d' % i).encode('utf-8'),
        properties={"key1": "val1", "key2": "val2"},
        partition_key='my-key')     

client.close()    









# import pulsar

# if __name__ == '__main__':
#     pass

# client = pulsar.Client('pulsar://pulsarbroker:6650')   

# producer = client.create_producer("persistent://public/default/my-topic",producer_name='my-python-producer',block_if_queue_full=True,batching_enabled=True,batching_max_publish_delay_ms=10)    
# print("producer sending data...............")
# for i in range(10):
#     producer.send(('Hello-%d' % i).encode('utf-8'),properties={"key1": "val1", "key2": "val2"},partition_key='my-key')     

# client.close()    
# print("producer closed connection...............")


# import string
# import pulsar
# # Create a pulsar client by supplying ip address and port
# client = pulsar.Client('pulsar://pulsarbroker:6650')
# # Create a producer on the topic that consumer can subscribe to
# producer = client.create_producer('C1-Topic',block_if_queue_full=True,batching_enabled=True,batching_max_publish_delay_ms=10)
# #do split operation by space
# splitted_sentence='Welcome to Data Engineering Course!'.split(" ")
# number_of_words=len(splitted_sentence)
# # Send each word to topic

# def send_callback(res, msg):
#       print('Message published res=%s', res)

# producer.send_async(str(number_of_words).encode('utf-8'),send_callback)
# print("sending to broker....")
# for word in splitted_sentence:
#     print(word)
#     producer.send_async((word).encode('utf-8'),send_callback)

# print("completed....")
# # Destroy pulsar client
# client.close()