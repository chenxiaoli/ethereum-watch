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
        'virtual_host':"/",
        'user': 'user',
        'password': '1318',
        "port": 5672
    },
    'queue': {
        "new_eth_block_arrived_topic": "new_eth_block_arrived_topic",  # 新区块产生
        "eth_block_number_queue": "eth_block_number_queue",  # 区块信息解析
        "eth_transaction_queue":"eth_transaction_queue",  # 事务解析解析
        "new_eth_trades_queue": "new_eth_trades_queue",  # 新交易
        # "subscriptions_queue":["..."],#订阅队列
    },
    "web3_provider":{
        "type":"http",
        "path":'http://eth-mainnet.tokenhub.cc:8515',

    },
    "start_block_number":10000
}
