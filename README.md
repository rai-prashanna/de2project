# GitHub analytic system using the streaming framework Pulsar | Project 2 | Team 3
This repository is part of the Data Engineering Course 2 at the Uppsala University
In this repository, we developed a Github analytic system to crawl data, process it, and produce targeted results using the Pulsar streaming framework. 

## Overview
. <br/>
├── multi-node-docker-deployment    <br/>
│   ├── aggregation                <br/>
│   ├── consumers          <br/>
│   ├── filter    <br/>
│   ├── mongo       <br/>
│   ├── producers   <br/> 
│   ├── pulsario        <br/>
│   └── docker-compose.yml  <br/>
├── single-node-docker-deployment <br/>
│   ├── aggregation         <br/>
│   ├── consumers          <br/>
│   ├── filter    <br/>
│   ├── mongo<br/>
│   ├── producers <br/>
│   ├── pulsario       <br/> 
│   └── docker-compose.yml  <br/> 
├── source                        #Pulsar Logic    <br/>
└── README.md<br/>


## Getting Started in single node
* Pull Repository
```
git pull https://github.com/rai-prashanna/de2project.git
```
* Start docker-compose to 
```
cd single-node-docker-deployment 
docker-compose build --no-cache
docker-compose up
```
* Start PulsarIO connection to MongoDB
```
docker exec -it single-node-docker-deployment_pulsarbroker_1 /pulsar/bin/pulsar-admin sinks create --sink-type mongo --sink-config-file /home/mongodb-sink.yml --inputs DE2-result
```
### See Results
* Open Browser and see current results
```
http://<ip-address>:5000/
```
* See MongoDB to view data from MongoDB-express
```
http://<ip-address>:8081/
```
## Getting Started in mulit-node
* Create 6 instances in snic cloud

* Clone repository  
```
git pull https://github.com/rai-prashanna/de2project.git
```

* Start pulsar instance in one of the node 
```
cd multi-node-docker-deployment
docker-compose up   
```  
* Start producer instance in one of the node 
```
cd multi-node-docker-deployment/producers
change IP to floating-Ip-of-pulsar-broker in config/extra-hosts-producers.yaml 
docker-compose -f docker-compose.yml -f config/extra-hosts-producers.yaml up
```
* Start filter instance in one of the node 
```
cd multi-node-docker-deployment/filter
change IP to floating-Ip-of-pulsar-broker in config/extra-hosts-filter.yaml
docker-compose -f docker-compose.yml -f config/extra-hosts-filter.yaml up
```

* Start consumer instance in one of the node 
```
cd multi-node-docker-deployment/consumers
change IP to floating-Ip-of-pulsar-broker in config/extra-hosts-consumers.yaml
docker-compose -f docker-compose.yml -f config/extra-hosts-consumers.yaml up
```
* Start aggregation instance in one of the node 
```
cd multi-node-docker-deployment/aggregation
change IP to floating-Ip-of-pulsar-broker in config/extra-hosts-aggregation.yaml
docker-compose -f docker-compose.yml -f config/extra-hosts-aggregation.yaml up
```
* Start MongoDB instance in one of the node 
```
cd multi-node-docker-deployment/mongo
docker-compose -f docker-compose.yml up
```
* Start Frontend instance in one of the node 
```
cd multi-node-docker-deployment/frontend
change IP to floating-Ip-of-mongoDB in config/extra-hosts-aggregation.yaml
docker-compose -f docker-compose.yml -f config/extra-hosts-app.yaml up
```
* Start PulsarIO connection to MongoDB from PulsarInstance
```
docker exec -it <Pulsar-container-ID> /pulsar/bin/pulsar-admin sinks create --sink-type mongo --sink-config-file /home/mongodb-sink.yml --inputs DE2-result
```
