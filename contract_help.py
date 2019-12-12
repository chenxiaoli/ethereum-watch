import time
from web3_config.web3_instance import get_web3_instance
from utils import rabbitmq_instance
import logging
from db.models import Block
from utils import block as block_utils
from db import services as db_services
import json
from web3 import Web3
import abi



if __name__ == '__main__':

    encrypted_key=""" '{"version":3,"id":"660c97bf-4ea5-4094-8bbd-79444ccab288","address":"4401a56df8e8e209ae594ac3308e26b5957d1229","crypto":{"ciphertext":"f4e7852a2ca6a50cd57d86b01b24aa14b33a0b213b10a8de256c57c479ce929f","cipherparams":{"iv":"e3487f4ecf012f324960f1ab14e2219d"},"cipher":"aes-128-ctr","kdf":"scrypt","kdfparams":{"dklen":32,"salt":"4ad5971877271ba8e8b6a88758a629d474aa794dfac7debd68d833612ebcbb28","n":8192,"r":8,"p":1},"mac":"029c25ff9ee9a08c800bc9f766030823c81e6a4a8e427dec4f105b968633df0d"}}' }"""

    w3 = get_web3_instance()
    contract_address=Web3.toChecksumAddress("0xFc690e0a59ddB30341e05991255B06405A4337AD")
    sending_address=Web3.toChecksumAddress("0x4401a56df8e8e209ae594ac3308e26b5957d1229")

    private_key = "0x7ea8199981e6cec24a9a76cf19cdba457452fc7c9c16a582c0f0d4c866e573e9"

    nonce =15
    #nonce = w3.eth.getTransactionCount(sending_address, "pending")

    print("nonce:",nonce)
    contract = w3.eth.contract(address=contract_address,abi=abi.tfor_abi)
    print(contract.all_functions())
    value=1*10**6
    print(value)

    print(contract.functions.CurrentOwner().call())

    # gas_price=w3.eth.generateGasPrice()*1.5
    # tx_hash = contract.functions.withdraw_aaa(value).buildTransaction({
    # 'chainId': 1,
    # 'nonce': nonce,
    #     'gas': 900000,
    #     'gasPrice': gas_price,
    # })
    # tx_hash = contract.functions.transferOwnership(sending_address).buildTransaction({
    # 'chainId': 1,
    # 'nonce': nonce,
    #     'gas': 900000,
    #     'gasPrice': gas_price,
    # })

    # signed_txn=w3.eth.account.sign_transaction(tx_hash, private_key=private_key)
    # print("signed_txn:",signed_txn)
    # transaction_hash=w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    # print("transaction_hash:",Web3.toHex(transaction_hash))
    #
    # tx_receipt = w3.eth.waitForTransactionReceipt(transaction_hash)
    # print("tx_receipt:",tx_receipt)
    #0x3656c1528883fb12167adc7f347ecde77dd42b6e609013144abc6558e6921c44
    #b'6V\xc1R\x88\x83\xfb\x12\x16z\xdc\x7f4~\xcd\xe7}\xd4+n`\x90\x13\x14J\xbceX\xe6\x92\x1cD'

