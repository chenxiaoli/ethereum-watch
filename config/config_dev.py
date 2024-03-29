configs = {
    'env': 'dev',
    'db': {
        'db_name': 'ethereum-watch-dev',
        'username': 'ethereum-watch-dev',
        'password': 'xxx',
        'host': '192.168.8.126',
        'port': 27017,
    },
    'rabbitmq_server': {
        'host': '192.168.8.126',
        'virtual_host':"/ethereum-watch-dev",
        'user': 'ethereum-watch-dev',
        'password': 'xxx',
        "port": 5672
    },
    'queue': {
        "new_eth_block_arrived_topic": "new_eth_block_arrived_topic",  # 新区块产生
        "eth_block_number_queue": "eth_block_number_queue",  # 区块信息解析
        "eth_transaction_queue":"eth_transaction_queue",  # 事务解析解析
        "new_ethereum_trade_exchange": "new_ethereum_trade_exchange"  # 新交易
        # "subscriptions_queue":["..."],#订阅队列
    },
    "web3_provider":{
        "type":"http",
        "path":'http://xxx:8515',

    },
    "start_block_number":1
}
