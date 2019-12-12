from web3 import Web3
from web3_config.web3_instance import get_web3_instance


def parse_transaction(transaction):
    w3 = get_web3_instance()
    trades = []
    from_address = transaction.get("from")
    to_address = transaction.get("to")
    value = w3.fromWei(transaction["value"], 'ether')  # 这里注意溢出
    block_number = transaction.get("blockNumber")
    transaction_hash = w3.toHex(transaction.get("hash"))
    if from_address and to_address and value:
        trades.append(
            {"from": from_address, "to": to_address, "value": float(value), "symbol": "eth",
             "block_number": block_number,
             "transaction_hash": transaction_hash})
    logs = transaction.get("logs", None)
    if transaction.get(
            "logs"):  # 智能合约(erc20) logs中，topics[0]都是事件的keccka的hash结果；topics[1]topics[2]分别是from和to；address是合约地址；data是交易额；
        contract_address = logs.get("address", None)
        topics = logs.get("topics", None)
        data = logs.get("data", 0)
        if contract_address and topics and data:
            from_address = topics[1]

            to_address = topics[2]
            data = Web3.toInt(logs.data)  # 这里可能会出现异常,溢出
            trades.append(
                {"from": from_address, "to": to_address, "value": data, "contract_address": contract_address,
                 "block_number": block_number, "transaction_hash": transaction_hash})
    return trades

def parse_transaction_receipt(transaction_receipt):
    w3 = get_web3_instance()
    trades = []

    block_number = transaction_receipt.get("blockNumber")
    transaction_hash = w3.toHex(transaction_receipt.get("transactionHash"))
    if transaction_receipt.get("status")!=1:
        return []
    logs = transaction_receipt.get("logs", None)
    for log in logs:
                     # 智能合约(erc20) logs中，topics[0]都是事件的keccka的hash结果；topics[1]topics[2]分别是from和to；address是合约地址；data是交易额；
            contract_address = log.get("address", None)
            topics = log.get("topics", None)
            data = log.get("data", 0)
            if contract_address and topics and data:
                from_address = topics[1]
                to_address = topics[2]
                print("bytes:", len(from_address))

                from_address=Web3.toHex(from_address[-20:])
                to_address=Web3.toHex(to_address[-20:])
                print("from:",from_address)
                print("to:", to_address)
                data = Web3.toInt(hexstr=log.data)  # 这里可能会出现异常,溢出
                print("data:", type(transaction_hash))
                trades.append(
                    {"from": from_address, "to": to_address, "value": data, "contract_address": contract_address,
                     "block_number": block_number, "transaction_hash": transaction_hash})
    return trades

