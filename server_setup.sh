#!/bin/bash
echo ">>> Uninstalling Old Docker versions"
sudo apt-get remove docker docker-engine docker.io containerd runc

echo ">>> Updating system"
sudo apt-get update

echo ">>> Install neccessary packages"
sudo apt-get install ca-certificates curl gnupg lsb-release -y

echo ">>> Adding docker's official GPG key"
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo ">>> Setting up repo for Docker"
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo ">>> Updating package index"
sudo apt-get update

echo ">>> Installing Docker Engine"
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

echo ">>> Adding USER to docker group"
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

echo ">>> Checking DOCKER installation"
docker run hello-world
docker -v
docker compose version
