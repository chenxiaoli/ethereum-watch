from threading import Thread
import time
from web3_config.web3_instance import get_web3_instance
from utils import rabbitmq_instance
import logging

from utils import block as block_utils
from db import services as db_services
import json


def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Change this to DEBUG if you want a lot more info
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


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


def new_block_process(block_number):
    db_latest_block_number = db_services.get_latest_block_number()
    if block_number > db_latest_block_number:
        for pre_number in range(db_latest_block_number, block_number + 1):
            block_process(pre_number)
    else:
        block_process(block_number)


def handle_event(event):
    block_number = w3.eth.blockNumber
    new_block_process(block_number)


def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)


class MyDaemon(Thread):
    def run(self):
        # 如果数据库的高度跟当前区块高度不一致,应该触发一个业务把丢失的区块处理了.
        latest_block_filter = w3.eth.filter('latest')
        log_loop(latest_block_filter, 2)


if __name__ == '__main__':
    setup_logger()
    block_number = w3.eth.blockNumber
    db_latest_block_number = db_services.get_latest_block_number()
    if block_number > db_latest_block_number:
        for pre_number in range(db_latest_block_number, block_number + 1):
            block_process(pre_number)

    t = MyDaemon()
    t.deamon = True
    t.start()
    while True:
        if not t.is_alive():
            t = MyDaemon()
            t.deamon = True
            t.start()
        time.sleep(10)
