import time
from web3_config.web3_instance import get_web3_instance
import logging
from config import configs as myconfig
from web3 import Web3

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



def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            print(event)
        time.sleep(poll_interval)



def run():
    # 如果数据库的高度跟当前区块高度不一致,应该触发一个业务把丢失的区块处理了.
    event_signature_hash = Web3.keccak(text="Transfer(address,address,uint256)").hex()
    latest_block_filter = w3.eth.filter({"topics":[event_signature_hash,None,"0x00000000000000000000000015BadD16B9D198D46AE98F2d25F451788794C9B1"]})
    print(latest_block_filter)
    log_loop(latest_block_filter,3)



if __name__ == '__main__':
    run()
