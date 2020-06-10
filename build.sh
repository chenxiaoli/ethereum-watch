#!/bin/bash
echo "start build"
if [ $1 = "dev" ];then
  cp ./config_dev.py ./config/config_dev.py
elif [ $1 = "prod" ]; then
  cp ./config_prod.py ./config/config_dev.py
fi
sudo docker build --tag=ethereum-watch .

