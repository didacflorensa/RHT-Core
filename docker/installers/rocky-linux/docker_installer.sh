#!/bin/bash

sudo yum check-update
yum install dnf -y
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

dnf update
dnf install -y docker-ce docker-ce-cli containerd.io
#sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

#sudo yum install docker-ce-20.10.11 -y
sudo systemctl start docker
sudo systemctl enable docker

sudo systemctl status docker


# Installing docker-compose. Specify the version in the next line
sudo curl -L "https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version
