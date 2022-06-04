# GitHub analytic system using the streaming framework Pulsar | Project 2 | Team 3
This repository is part of the Data Engineering Course 2 at the Uppsala University
In this repository, we developed a Github analytic system to crawl data, process it, and produce targeted results using the Pulsar streaming framework. 

## Overview
.
├── docker                  # Finaly Version of the implemented approach
│   ├── aggregation         # Layer3: Aggregation consumer
│   ├── consumers           # Layer2
│   ├── filter    
│   ├── mongo
│   ├── producers    
│   ├── pulsario    
│   ├── cloud-init-lb.yml    
│   └── docker-compose.yml  # Unit tests
├── source                     # Source files (alternatively `lib` or `app`)
├── standalone_with_docker  # Automated tests (alternatively `spec` or `tests`)
└── README.md

## Getting Started
### Dependencies
* Pull Repository
```
git pull https://github.com/rai-prashanna/de2project.git
```
* Start docker-compose to 
```
cd docker
docker-compose up --build
```
