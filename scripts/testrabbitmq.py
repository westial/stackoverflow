#!/usr/bin/env python
"""Basic test case for rabbitmq health.

Client A posts a job to Queue and Client B gets the content from.

Usage:

    $ python testrabbitmq.py

Requirements:

    * python 2.7
    * pika
    * unitest
"""
import unittest
from Queue import Queue
from thread import start_new_thread

import pika
import time

"""Configuration below works for default RabbitMQ installation."""
HOST = '127.0.0.1'
USER = 'guest'
PASSWORD = 'guest'
QUEUE = 'hello'
MESSAGE = 'Hello World!'
EXCHANGE = ''
TIMEOUT = 5


class TestRabbitMq(unittest.TestCase):

    def setUp(self):
        self._received = Queue()
        self._receiver = None

    def test_hello(self):
        self._post_message()
        self._receive_message()
        spent = 0
        while spent <= TIMEOUT:
            if not self._received.empty():
                message = self._received.get()
                print('Consumer received "{!s}"'.format(message))
                self.assertEqual(
                        message,
                        MESSAGE
                )
                break
            spent += 1
            time.sleep(1)
        self.exit()

    def callback(self, ch, method, properties, body):
        self._received.put(body)

    def exit(self):
        """Gracefully stops receiver"""
        self.channel._cancel_all_consumers()

    def _async_receiver(self, callback):
        """Asynchronous connection to receive the message

        Args:
            callback: object function
        """
        print('Consumer is connecting to RabbitMQ...')
        self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=HOST)
        )
        print('Consumer is connected')
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=QUEUE)
        self.channel.basic_consume(
            callback,
            queue=QUEUE,
            no_ack=True
        )
        print('Consumer is starting consuming...')
        self.channel.start_consuming()

    def _receive_message(self):
        """Client B receives message"""
        start_new_thread(self._async_receiver, (self.callback, ))

    @classmethod
    def _post_message(cls):
        """Client A posts message"""
        print('Emitter is connecting to RabbitMQ...')
        connection = pika.BlockingConnection(
                pika.ConnectionParameters(HOST)
        )
        print('Emitter is connected')
        emitter_channel = connection.channel()
        emitter_channel.queue_declare(queue=QUEUE)
        print('Emitter is publishing content...')
        emitter_channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=QUEUE,
                body=MESSAGE
        )
        print('Emitter published content')
        connection.close()
        print('Emitter closed connection')


if __name__ == '__main__':
    unittest.main()
