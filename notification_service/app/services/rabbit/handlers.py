import pika


def register_user(channel: pika.adapters.blocking_connection.BlockingChannel, method, properties, body):
    print(66666666666666666666666666666666666666666666666)
    print(body, 121221212121212212212121)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def user_added_product_to_cart(channel: pika.adapters.blocking_connection.BlockingChannel, method, properties, body):
    print(777777777777777777777777777777)
    channel.basic_ack(delivery_tag=method.delivery_tag)
    