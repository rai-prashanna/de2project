#!/bin/bash
# sudo apt-get update -y
# sudo apt-get install git-lfs -y
sudo apt-get update
sudo apt-get install docker -y
sudo apt-get install docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -G docker ubuntu

#git clone https://github.com/scaleoutsystems/fedn.git
#chown -R ubuntu:ubuntu /home/ubuntu/fedn
#cd fedn
#git checkout develop
#develop
#chown -R ubuntu:ubuntu /home/ubuntu/fedn/*
sudo shutdown -r 1
