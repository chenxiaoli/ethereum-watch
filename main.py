import time
from web3_config.web3_instance import get_web3_instance
from utils import rabbitmq_instance
import logging
from db.models import Block
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


def new_block_process(block_number):
    block = w3.eth.getBlock(block_number)
    db_services.insert_block(block)
    logging.debug("new block %s" % block.number)
    for transaction_hash in block.transactions:
        transaction = w3.eth.getTransaction(transaction_hash)  # 遇性能问题,改异步把交易写入数据库,1.解析交易,发送到消息队列,2.保存transaction 到 数据库.
        trades = block_utils.parse_transaction(transaction)
        rabbitmq_instance.send_new_eth_trades_notification(json.dumps(trades))  # 发送交易通知到队列
        db_services.insert_transaction(transaction)
        db_services.transaction_to_account_detail(transaction)  # 解析交易数据到数据库


def handle_event(event):
    block_number = w3.eth.blockNumber
    new_block_process(block_number)


def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)


def run():
    latest_block_filter = w3.eth.filter('latest')
    log_loop(latest_block_filter, 2)


if __name__ == '__main__':
    setup_logger()
    run()
