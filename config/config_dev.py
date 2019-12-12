configs = {
    'env': 'dev',
    'db': {
        'db_name': 'ethereum-watch',
        'username': 'admin',
        'password': '1025',
        'host': '192.168.8.126',
        'port': 27017,
    },
    'rabbitmq_server': {
        'host': '192.168.8.126',
        'user': 'user',
        'password': '1318',
        "port": 5672
    },
    'queue': {
        "new_eth_block_arrived": "new_eth_block_arrived",  # 新区块产生
        "new_eth_trades_queue": "new_eth_trades_queue"  # 新交易
    },
    "web3_provider":{
        "type":"http",
        "path":'http://192.168.8.126:8546',
        #"path":"http://192.168.8.126:8545"
    }
}
