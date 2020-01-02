import pika

from config import configs as myconfig

rabbitmq_conn = None

NEW_ETH_BLOCK_CHANNEL = myconfig.configs.queue.new_eth_block_arrived_topic
NEW_ETH_TRADES_QUEUE = myconfig.configs.queue.new_eth_trades_queue
ETH_BLOCK_NUMBER_QUEUE = myconfig.configs.queue.eth_block_number_queue


def send_new_eth_block_notification(eth_tx_jsonStr):
    connection = get_rabbitmq_conn()
    eth_block_tx_channel = connection.channel()

    eth_block_tx_channel.exchange_declare(exchange=NEW_ETH_BLOCK_CHANNEL,

                                          exchange_type='fanout')

    eth_block_tx_channel.basic_publish(exchange=NEW_ETH_BLOCK_CHANNEL,
                                       routing_key="",
                                       body=eth_tx_jsonStr,
                                       )
    eth_block_tx_channel.close()


def send_eth_block_number(block_number):
    connection = get_rabbitmq_conn()
    channel = connection.channel()

    channel.queue_declare(queue=ETH_BLOCK_NUMBER_QUEUE, durable=True)

    channel.basic_publish(exchange="",
                          routing_key=ETH_BLOCK_NUMBER_QUEUE,
                          body=block_number,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    channel.close()



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

    if rabbitmq_conn is not None and not rabbitmq_conn.is_closed:
        return rabbitmq_conn
    else:
        credentials = pika.PlainCredentials(myconfig.configs.rabbitmq_server.user,
                                            myconfig.configs.rabbitmq_server.password)
        rabbitmq_conn = pika.BlockingConnection(pika.ConnectionParameters(
            host=myconfig.configs.rabbitmq_server.host, port=myconfig.configs.rabbitmq_server.port,
            virtual_host=myconfig.configs.rabbitmq_server.virtual_host,
            credentials=credentials
        )

        )

        return rabbitmq_conn
