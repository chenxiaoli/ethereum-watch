from threading import Thread
import time
from web3_config.web3_instance import get_web3_instance
from utils import rabbitmq_instance
import logging

from utils import block as block_utils
from db import services as db_services
import json
w3 = get_web3_instance()


def block_process(block_number):

    block = w3.eth.getBlock(block_number)
    db_services.insert_block(block)
    rabbitmq_instance.send_new_eth_block_notification(json.dumps({"number": block_number}))
    logging.debug("new block %s" % block.number)
    for transaction_hash in block.transactions:
        # 遇性能问题, 这里几个业务可以改成异步处理
        transaction = w3.eth.getTransaction(transaction_hash)
        transaction_receipt = w3.eth.getTransactionReceipt(transaction_hash)
        transaction_status = transaction_receipt.get("status")

        db_services.insert_transaction(transaction, transaction_receipt)
        trades = block_utils.parse_transaction(transaction)
        contract_trades = block_utils.parse_transaction_receipt(transaction_receipt)
        trades_count = len(trades)
        if transaction_status == 1:
            if trades_count == 1:
                rabbitmq_instance.send_new_eth_trades_notification(json.dumps(trades[0]))  # 发送交易通知到队列
                db_services.save_trade(trades[0])  # 解析交易数据到数据库
            elif trades_count > 1:
                print("error trades")

            for trade in contract_trades:
                rabbitmq_instance.send_new_eth_trades_notification(json.dumps(trade))  # 发送交易通知到队列

                db_services.save_trade(trade)  # 解析交易数据到数据库


if __name__ == '__main__':
    block_process(9128859)

