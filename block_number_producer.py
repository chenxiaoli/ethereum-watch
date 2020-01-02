from threading import Thread
import time
from web3_config.web3_instance import get_web3_instance
import logging

from db import services as db_services
from config import configs as myconfig
from utils import rabbitmq_instance

START_BLOCK = myconfig.configs.start_block_number


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
    db_latest_block_number = db_services.get_latest_block_number()
    print("block_number(%s)-db_latest_block_number(%s)=%s" % (
    block_number, db_latest_block_number, block_number - db_latest_block_number))
    if block_number < START_BLOCK:
        print("ignore block number")
        return

    for pre_number in range(db_latest_block_number+1, block_number+1):
        rabbitmq_instance.send_eth_block_number(str(pre_number))
        print("sent block number:", pre_number)
        db_services.insert_block({"number": pre_number})


def handle_event(event):
    block_number = w3.eth.blockNumber
    new_block_process(block_number)


def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)


def run():
    # 如果数据库的高度跟当前区块高度不一致,应该触发一个业务把丢失的区块处理了.
    latest_block_filter = w3.eth.filter('latest')
    log_loop(latest_block_filter, 2)


if __name__ == '__main__':
    run()
