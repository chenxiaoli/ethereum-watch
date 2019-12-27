import time
from web3_config.web3_instance import get_web3_instance
from utils import rabbitmq_instance
import logging
from db.models import Block
from utils import block as block_utils
from db import services as db_services
import json
import abi
from web3 import Web3


if __name__ == '__main__':

    w3 = get_web3_instance()


    # w3.eth.defaultAccount = w3.eth.accounts[0]
    # w3.geth.personal.unlockAccount(w3.eth.defaultAccount, "123")

    contract_address = "0x3382a696e01d6776a7585b08ac38071c2f1d2ccf"
    contract_address = Web3.toChecksumAddress(contract_address)
    contract = w3.eth.contract(address=contract_address, abi=abi.tfor_abi)
    print(contract.all_functions())
    print(contract.functions.decimals().call())
