import time
from web3_config.web3_instance import get_web3_instance
from utils import rabbitmq_instance
import logging
from db.models import Block
from utils import block as block_utils
from db import services as db_services
import json


def block_process(block_number):
    w3 = get_web3_instance()
    block = w3.eth.getBlock(block_number)
    db_services.insert_block(block)
    logging.debug("new block %s" % block.number)
    for transaction_hash in block.transactions:
        # 遇性能问题, 这里几个业务可以改成异步处理
        transaction = w3.eth.getTransaction(transaction_hash)
        db_services.insert_transaction(transaction)
        transaction_receipt = w3.eth.getTransactionReceipt(transaction_hash)
        print("transaction_receipt:", transaction_receipt)
        trades = block_utils.parse_transaction_receipt(transaction_receipt)
        print(trades)
        rabbitmq_instance.send_new_eth_trades_notification(json.dumps(trades))  # 发送交易通知到队列

        db_services.transaction_to_account_detail(transaction)  # 解析交易数据到数据库


if __name__ == '__main__':
    block_process(16206)

