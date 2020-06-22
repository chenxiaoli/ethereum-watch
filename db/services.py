from db.conn import db
from mongoengine.errors import NotUniqueError
from mongoengine.errors import DoesNotExist
from web3_config import web3_instance
from web3 import Web3
from .models import Transaction
from .models import Block
from .models import AccountDetail
from .models import Account
from .models import Token
from .models import ExceptionTransaction
from web3_config.web3_instance import get_web3_instance
from utils import block as block_utils
from bson import decimal128
from db.constants import MAX_TRADE_VALUE
from contract.erc20 import Erc20
import pymongo


def _format_transaction(transaction):
    _t = {}
    currency = "ether"
    w3 = web3_instance.get_web3_instance()
    value = w3.fromWei(transaction["value"], 'ether')
    _t.update(transaction)
    _t.update({"value": float(value), "currency": currency})

    # if transaction["value"] > 2 ** 63 - 1:
    #     _t.update({"value": Decimal128(Decimal(str(transaction["value"])))})
    return _t


def insert_transaction(transaction, transaction_receipt):
    w3 = web3_instance.get_web3_instance()
    block_number = transaction.get("blockNumber")
    transaction_hash = w3.toHex(transaction.get("hash"))
    data = _format_transaction(transaction)
    db_o = Transaction(data=data, block_number=block_number,
                       transaction_hash=transaction_hash, transaction_receipt=transaction_receipt)
    try:
        db_o.save()
    except NotUniqueError:
        ExceptionTransaction(data=data, block_number=block_number,
                             transaction_hash=transaction_hash).save()


def get_latest_block_number():
    last = Block.objects().order_by("-number").first()
    if not last:
        return 0
    else:
        return last.number


def insert_block(block):
    number = block.get("number")
    try:
        _block = Block(data={}, number=number)
        _block.save()
        return True
    except NotUniqueError:
        return False


def update_block(block):
    number = block.get("number")
    _block = Block.objects(number=number).first()
    if _block:
        _block.read_done = "YES"
        _block.save()


def parse_transaction_to_account_detail(transaction):
    """解析transaction的交易"""
    account_detail_list = []
    from_address = transaction.get("from")
    to_address = transaction.get("to")
    value = transaction.get("value")
    if from_address and to_address and value:
        account_detail_list.append({"from": from_address, "to": to_address, "value": value, "symbol": "eth"})
    logs = transaction.get("logs", None)
    if transaction.get(
            "logs"):  # 智能合约(erc20) logs中，topics[0]都是事件的keccka的hash结果；topics[1]topics[2]分别是from和to；address是合约地址；data是交易额；
        contract_address = logs.get("address", None)
        topics = logs.get("topics", None)
        data = logs.get("data", 0)
        if contract_address and topics and data:
            from_address = topics[1]
            to_address = topics[2]
            data = Web3.toInt(logs.data)  # 这里可能会出现异常
            account_detail_list.append(
                {"from": from_address, "to": to_address, "value": data, "contract_address": contract_address})
    return account_detail_list


def get_token_by_address(address):
    try:
        token = Token.objects.get(contract_address=address)
        return token
    except DoesNotExist:
        return


def contract_balance_of(address, contract_address, abi, decimals):
    w3 = get_web3_instance()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    receiver = Web3.toChecksumAddress(address)
    return contract.functions.balanceOf(receiver).call() / (10 ** decimals)


def get_eth_balance(address):
    w3 = get_web3_instance()
    return w3.fromWei(w3.eth.getBalance(address), 'ether')


def transaction_to_account_detail(transaction):
    """
        1.把transaction数据解析
        2.account detail 保存
        3.更新account 余额
        4.交易通知发送
    """
    account_detail_list = block_utils.parse_transaction(transaction)
    for account_detail_map in account_detail_list:
        account_detail = AccountDetail()
        account_detail.block_number = transaction.blockNumber
        account_detail.transaction_hash = account_detail_map.get("transaction_hash")
        account_detail.from_address = account_detail_map.get("from")
        account_detail.to_address = account_detail_map.get("to")
        account_detail.value = account_detail_map.get("value")
        account_detail.symbol = account_detail_map.get("symbol", None)
        account_detail.symbol_contract_address = account_detail_map.get("contract_address", None)
        if account_detail.symbol_contract_address:
            token = get_token_by_address(account_detail.contract_address)
            if token:
                account_detail.value = account_detail.value / (10 ** token.decimals)
                account_detail.symbol = token.symbol
                account_detail.save()
                update_account_balance(account_detail, token)
        else:
            account_detail.save()
            update_account_balance(account_detail)


def update_account_balance(account_detail, token=None):
    """通过节点数据查询更新账户余额"""
    try:
        from_account = Account.objects.get(address=account_detail.from_address)
    except DoesNotExist:
        from_account = Account(address=account_detail.from_address, eth_balance=0)
        from_account.save()
    try:
        to_account = Account.objects.get(address=account_detail.to_address)
    except DoesNotExist:
        to_account = Account(address=account_detail.to_address, eth_balance=0)
        to_account.save()
    if token:
        balance1 = contract_balance_of(address=account_detail.from_address,
                                       contract_address=account_detail.symbol_contract_address, abi=token.abi,
                                       decimals=token.decimals)
        from_account.update_balance(balance1, account_detail.symbol_contract_address)

        balance2 = contract_balance_of(address=account_detail.to_address,
                                       contract_address=account_detail.symbol_contract_address, abi=token.abi,
                                       decimals=token.decimals)
        to_account.update_token_balance(balance2, token)
    else:
        balance1 = get_eth_balance(account_detail.from_address)
        from_account.eth_balance = balance1
        from_account.save()
        balance2 = get_eth_balance(account_detail.to_address)
        to_account.eth_balance = balance2
        to_account.save()


def save_trade(trade):
    # {"from": from_address, "to": to_address, "value": data, "contract_address": contract_address,
    #  "block_number": block_number, "transaction_hash": transaction_hash})

    # print("-----start save trade --------")
    value = trade["value"]
    if type(value) == int and MAX_TRADE_VALUE < value:
        one = {}
        one.update({"value": str(trade["value"])})
        one.update({"transaction_hash": trade["transaction_hash"]})
        one.update({"from_address": trade["from"]})
        one.update({"to_address": trade["from"]})
        one.update({"contract_address": trade.get("contract_address", None)})
        one.update({"block_number": trade["block_number"]})
        try:
            db.exception_trade.insert_one(one)
        except pymongo.errors.DuplicateKeyError:
            pass
    # one = db.account_detail.find_one({"transaction_hash": trade["transaction_hash"]})
    # print(one)
    else:
        one = {}
        one.update({"value": decimal128.Decimal128(str(trade["value"]))})
        one.update({"transaction_hash": trade["transaction_hash"]})
        one.update({"from_address": trade["from"]})
        one.update({"to_address": trade["from"]})
        one.update({"contract_address": trade.get("contract_address", None)})
        one.update({"block_number": trade["block_number"]})
        try:
            db.account_detail.insert_one(one)
        except pymongo.errors.DuplicateKeyError:
            pass


def get_contract_info(address):
    token = Token.objects(contract_address=address).first()
    if token:
        return token
    erc20 = Erc20(address=address)
    contract_info = erc20.contract_info
    name = contract_info.get("name")
    symbol = contract_info.get("symbol")
    decimals = contract_info.get("decimals")
    total_supply = contract_info.get("totalSupply")
    token = Token(name=name, symbol=symbol, decimals=decimals, total_supply=total_supply)
    if token.name and symbol and str(decimals).isdigit():
        try:
            token.save()
        except pymongo.errors.DuplicateKeyError:
            pass
        return token
    return None
