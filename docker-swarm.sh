sudo usermod -aG docker $USER
newgrp docker 

docker swarm init --advertise-addr 130.238.29.28
docker swarm join --token SWMTKN-1-6bes5mlokr6yg25jwx7dzak25rjjsogrnouzzu32gqgrwdf2cj-7fitbipvw7lom1ezwnaqs1ivu 130.238.29.28:2377
