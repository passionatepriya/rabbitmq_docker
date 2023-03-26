#!/usr/bin/env python3 -u
import pika

def callback(ch, method, properties, body):
    print(f" [x] Received '{body.decode()}'")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq-server'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()