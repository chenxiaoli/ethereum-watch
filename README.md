# ethereum-watch
以太坊区块监听程序

环境配置
1.创建一个独立的Python运行环境,命名为venv
virtualenv --python=/usr/bin/python3.6 ./venv
安装依赖包
pip install -r requirements.txt
安装 rabbmitmq
sudo docker run -d --hostname eth-rabbit --name rabbit -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=1318 \
 -p 15671:15671 \
 -p 15672:15672 \
  -p 5671:5671 \
  -p 5672:5672 \
 -p 25672:25672 \
rabbitmq:3-management

http://192.168.8.126:15672


sudo docker build --tag=ethereum-watch .

docker stack deploy -c docker-compose.yaml ethereum-watch
docker stack deploy -c docker-compose.yaml ethereum-watch-prod
