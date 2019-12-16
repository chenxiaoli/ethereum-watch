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




if __name__ == '__main__':
    rabbitmq_instance.send_new_eth_trades_notification(json.dumps({"fff":"test"}))  # 发送交易通知到队列