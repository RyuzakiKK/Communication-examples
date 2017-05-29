from twisted.internet import reactor
from wormhole.cli.public_relay import RENDEZVOUS_RELAY
import wormhole
import gi
import logging
gi.require_version('Gtk', '3.0')
from gi.repository import GLib


logger = logging.getLogger(__name__)
server_socket = None

w2 = None
w1 = None


def send(message, callback1, callback2):
    global w2
    logger.info("Sending a message")

    w2 = wormhole.create(u"wormgui", RENDEZVOUS_RELAY, reactor)
    w2.allocate_code()

    def write_code(code):
        logger.info("Invitation Code:", code)
        GLib.idle_add(callback1, code)

    w2.get_code().addCallback(write_code)
    w2.send_message(str.encode(message))

    # wait for reply
    def received(msg):
        logger.info("Got data, %d bytes" % len(msg))
        GLib.idle_add(callback2, True)
        w2.close()

    w2.get_message().addCallback(received)


def stop_sending(callback):
    global w2
    if w2 is not None:
        w2.close()

    GLib.idle_add(callback)


def start_receive(code, callback):
    global w1
    w1 = wormhole.create(u"wormgui", RENDEZVOUS_RELAY, reactor)
    w1.set_code(code)

    def received(message):
        logger.info("Message received:", message)
        GLib.idle_add(callback, message)
        return w1.send_message(b"outbound data")

    w1.get_message().addCallback(received)


def stop_receiving(callback):
    global w1
    if w1 is not None:
        w1.close()

    GLib.idle_add(callback)
