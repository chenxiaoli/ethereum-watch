from config import configs as myconfig
from web3 import Web3
import logging

_web3 = None


def get_web3_instance():
    global _web3
    if _web3 is not None:
        return _web3
    else:
        if myconfig.configs.env == "prod":
            my_provider = Web3.IPCProvider('/home/bill/eth-private-network/data2/geth.ipc')
        else:
            my_provider = Web3.IPCProvider('/home/bill/eth-private-network/data2/geth.ipc')
        _web3 = Web3(my_provider)

        logging.debug(".....start web3.....")
        return _web3
