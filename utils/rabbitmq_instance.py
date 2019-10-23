import pika

from config import configs as myconfig

rabbitmq_conn = None

NEW_ETH_BLOCK_CHANNEL = myconfig.configs.queue.new_eth_block_arrived
NEW_ETH_TRADES_QUEUE = myconfig.configs.queue.new_eth_trades_queue


def send_new_eth_block_notification(eth_tx_jsonStr):
    connection = get_rabbitmq_conn()
    eth_block_tx_channel = connection.channel()
    eth_block_tx_channel.queue_declare(queue=NEW_ETH_BLOCK_CHANNEL, durable=True)

    eth_block_tx_channel.basic_publish(exchange="",
                                       routing_key=NEW_ETH_BLOCK_CHANNEL,
                                       body=eth_tx_jsonStr,
                                       properties=pika.BasicProperties(
                                           delivery_mode=2,  # make message persistent
                                       ))
    eth_block_tx_channel.close()


def send_new_eth_trades_notification(trades_json):
    connection = get_rabbitmq_conn()
    channel = connection.channel()
    channel.queue_declare(queue=NEW_ETH_TRADES_QUEUE, durable=True)

    channel.basic_publish(exchange="",
                          routing_key=NEW_ETH_TRADES_QUEUE,
                          body=trades_json,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    channel.close()


def get_rabbitmq_conn():
    global rabbitmq_conn

    if rabbitmq_conn is not None:
        return rabbitmq_conn
    else:
        credentials = pika.PlainCredentials(myconfig.configs.rabbitmq_server.user,
                                            myconfig.configs.rabbitmq_server.password)
        rabbitmq_conn = pika.BlockingConnection(pika.ConnectionParameters(
            host=myconfig.configs.rabbitmq_server.host, port=myconfig.configs.rabbitmq_server.port,
            credentials=credentials)
        )
        return rabbitmq_conn
