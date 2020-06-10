from web3_config.web3_instance import get_web3_instance
from utils import rabbitmq_instance
import logging
import pika

from utils import block as block_utils
from db import services as db_services
import json
from config import configs as myconfig

w3 = get_web3_instance()

def block_process(block_number):

    block = w3.eth.getBlock(block_number)
    db_services.update_block(block)
    rabbitmq_instance.send_new_eth_block_notification(json.dumps({"number": block_number}))
    #print("new block %s" % block.number)
    logging.debug("new block %s" % block.number)
    for transaction_hash in block.transactions:
        transaction_hash = w3.toHex(transaction_hash)
        rabbitmq_instance.send_eth_transaction_notification(transaction_hash)


def on_message(channel, method_frame, header_frame, body):
    block_process(int(body))
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    user = myconfig.configs.rabbitmq_server.user
    password = myconfig.configs.rabbitmq_server.password
    host = myconfig.configs.rabbitmq_server.host
    port = myconfig.configs.rabbitmq_server.port
    eth_block_number_queue=myconfig.configs.queue.eth_block_number_queue
    vhost=myconfig.configs.rabbitmq_server.virtual_host

    credentials = pika.PlainCredentials(user, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host, port=port,vhost=vhost, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue=eth_block_number_queue, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(on_message, eth_block_number_queue)
    channel.start_consuming()

