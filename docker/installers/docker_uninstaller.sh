#!/bin/bash

sudo yum remove docker \
              docker-client \
              docker-client-latest \
              docker-common \
              docker-latest \
              docker-latest-logrotate \
              docker-logrotate \
              docker-engine

sudo rm -rf /var/lib/docker

sudo rm -rf /etc/docker


 #Remove docker-compose
 rm /usr/local/bin/docker-compose
