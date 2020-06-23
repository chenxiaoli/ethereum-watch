from web3.exceptions import TransactionNotFound
from web3_config.web3_instance import get_web3_instance
from utils import rabbitmq_instance
import logging
import pika

from utils import block as block_utils

import json
from config import configs as myconfig
from db import services

w3 = get_web3_instance()


def transaction_process(transaction_hash):
    # print("new block %s" % block.number)
    logging.debug("transaction hash %s" % transaction_hash)

    transaction_hash = transaction_hash.decode("utf8")
    # print(type(transaction_hash),transaction_hash)
    # 遇性能问题, 这里几个业务可以改成异步处理
    try:
        transaction = w3.eth.getTransaction(transaction_hash)
    except TransactionNotFound:
        logging.error("TransactionNotFound:%s" % transaction_hash)
        return

    try:
        transaction_receipt = w3.eth.getTransactionReceipt(transaction_hash)
    except TransactionNotFound:
        logging.error("TransactionNotFound:%s" % transaction_hash)
        return

    transaction_status = transaction_receipt.get("status")
    status = None
    if transaction_status == 1:
        status = "success"
    elif transaction_status == 0:
        status = "fail"

    trades = block_utils.parse_transaction(transaction)
    contract_trades = block_utils.parse_transaction_receipt(transaction_receipt)

    for trade in trades:
        trade.update({"status": status,
                      "chain_code":"ethereum",
                     })
    if len(trades) > 0:
        rabbitmq_instance.send_new_eth_trades_notification(json.dumps(trades))  # 发送交易通知到队列
    for trade in contract_trades:
        contract_address = trade.get("contract_address")
        token = services.get_contract_info(contract_address)
        trade.update({"name": token.name, "symbol": token.symbol, "decimals": token.decimals,
                      "total_supply": token.total_supply,"chain_code":"ethereum"})
        trade.update({"status": status})
    if len(contract_trades) > 0:
        rabbitmq_instance.send_new_eth_trades_notification(json.dumps(contract_trades))  # 发送交易通知到队列


def on_message(channel, method_frame, header_frame, body):
    transaction_process(body)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    user = myconfig.configs.rabbitmq_server.user
    password = myconfig.configs.rabbitmq_server.password
    host = myconfig.configs.rabbitmq_server.host
    port = myconfig.configs.rabbitmq_server.port
    virtual_host = myconfig.configs.rabbitmq_server.virtual_host
    eth_transaction_queue = myconfig.configs.queue.eth_transaction_queue

    credentials = pika.PlainCredentials(user, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host, port=port, virtual_host=virtual_host, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=eth_transaction_queue, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_message, eth_transaction_queue)
    channel.start_consuming()
