from config import configs as myconfig
from web3 import Web3
from web3 import Web3, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

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
            _web3.eth.setGasPriceStrategy(medium_gas_price_strategy)
            _web3.middleware_onion.add(middleware.time_based_cache_middleware)
            _web3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
            _web3.middleware_onion.add(middleware.simple_cache_middleware)

        elif myconfig.configs.web3_provider.type == "http":
            my_provider = Web3.HTTPProvider(myconfig.configs.web3_provider.path)
            _web3 = Web3(my_provider)
            _web3.eth.setGasPriceStrategy(medium_gas_price_strategy)
            _web3.middleware_onion.add(middleware.time_based_cache_middleware)
            _web3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
            _web3.middleware_onion.add(middleware.simple_cache_middleware)

        else:
            raise Exception("请配置ipc priovider")

        logging.debug(".....start web3.....")
        return _web3

