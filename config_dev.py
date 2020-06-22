configs = {
    'env': 'dev',
    'db': {
        'db_name': 'ethereum-watch-dev',
        'username': 'ethereum-watch-dev',
        'password': '1025',
        'host': '192.168.8.126',
        'port': 27017,
    },
    'rabbitmq_server': {
        'host': '192.168.8.126',
        'virtual_host':"/ethereum-watch-dev",
        'user': 'ethereum-watch-dev',
        'password': '13318',
        "port": 5672
    },
    'queue': {
        "new_eth_block_arrived_topic": "new_eth_block_arrived_topic",  # 新区块产生
        "eth_block_number_queue": "eth_block_number_queue",  # 区块信息解析
        "eth_transaction_queue":"eth_transaction_queue",  # 事务解析解析
        "new_eth_trades_queue": "new_eth_trades_queue"  # 新交易
    },
    "web3_provider":{
        "type":"http",
        "path":'http://192.168.8.126:8546',
        #"path":"http://192.168.8.126:8545",
    },
    "start_block_number":1
}
