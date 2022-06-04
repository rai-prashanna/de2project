# GitHub analytic system using the streaming framework Pulsar | Project 2 | Team 3
This repository is part of the Data Engineering Course 2 at the Uppsala University
In this repository, we developed a Github analytic system to crawl data, process it, and produce targeted results using the Pulsar streaming framework. 

## Overview
.
├── multi-node-docker-deployment
│   ├── aggregation         
│   ├── consumers          
│   ├── filter    
│   ├── mongo
│   ├── producers    
│   ├── pulsario        
│   └── docker-compose.yml  
├── single-node-docker-deployment    
│   ├── aggregation         
│   ├── consumers          
│   ├── filter    
│   ├── mongo
│   ├── producers    
│   ├── pulsario        
│   └── docker-compose.yml   
├── source  #Pulsar Logic               
└── README.md

## Getting Started
* Pull Repository
```
git pull https://github.com/rai-prashanna/de2project.git
```
* Start docker-compose to 
```
cd single-node-docker-deployment 
```
```
docker-compose up --build
```
* Start PulsarIO connection to MongoDB
```
docker exec -it single-node-docker-deployment_pulsarbroker_1 /bin/bash
```
```
/pulsar/bin/pulsar-admin sinks create --sink-type mongo --sink-config-file /home/mongodb-sink.yml --inputs DE2-result

```
