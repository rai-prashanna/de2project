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
