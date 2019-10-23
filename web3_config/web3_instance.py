from config import configs as myconfig
from web3 import Web3
import logging

_web3 = None


def get_web3_instance():
    global _web3
    if _web3 is not None:
        return _web3
    else:
        if myconfig.configs.web3_provider.type == "ipc":
            my_provider = Web3.IPCProvider(myconfig.configs.web3_provider.path)
            _web3 = Web3(my_provider)
        else:
            raise Exception("请配置ipc priovider")

        logging.debug(".....start web3.....")
        return _web3
