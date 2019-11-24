#!/bin/bash

program=matching

echo "Building container image for" ${program}
cd ${program} && sudo docker build -t ${program}:latest .

sudo docker run -t -d -h matching --restart=no --name matching matching
sudo docker exec -it matching bash -c "python3 matching.py"

docker rm -f matching
