from twisted.internet import reactor
from wormhole.cli.public_relay import RENDEZVOUS_RELAY
import wormhole
import gi
import logging
gi.require_version('Gtk', '3.0')
from gi.repository import GObject


logger = logging.getLogger(__name__)
server_socket = None

w2 = None
w1 = None


def send(code, message, callback):
    global w2
    logger.info("Sending a message")

    w2 = wormhole.create(u"wormgui", RENDEZVOUS_RELAY, reactor)
    w2.set_code(code)
    w2.send_message(str.encode(message))

    # wait for reply
    def received(msg):
        logger.info("Got data, %d bytes" % len(msg))
        GObject.idle_add(callback, True)
        w2.close()

    w2.get_message().addCallback(received)


def stop_sending(callback):
    global w2
    if w2 is not None:
        w2.close()

    GObject.idle_add(callback)


def start_receive(callback1, callback2):
    global w1
    w1 = wormhole.create(u"wormgui", RENDEZVOUS_RELAY, reactor)
    w1.allocate_code()

    def write_code(code):
        logger.info("code: %s" % code)
        _got_code(code, callback1)

    w1.get_code().addCallback(write_code)

    def received(msg):
        logger.info("got data, %d bytes" % len(msg))
        _got_message(msg, callback2)

    w1.get_message().addCallback(received)


def _got_code(code, callback):
    global w1
    logger.info("Invitation Code:", code)
    GObject.idle_add(callback, code)
    return w1.send_message(b"outbound data")


def _got_message(message, callback):
    logger.info("Message received:", message)
    GObject.idle_add(callback, message)


def stop_receiving(callback):
    global w1
    if w1 is not None:
        w1.close()

    GObject.idle_add(callback)
