from twisted.internet import reactor
from wormhole.cli.public_relay import RENDEZVOUS_RELAY
from wormhole.wormhole import wormhole
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
    logging.info("Sending a message")

    w2 = wormhole(u"wormgui", RENDEZVOUS_RELAY, reactor)
    w2.set_code(code)
    w2.send(str.encode(message))

    # wait for the reply
    d = w2.get()
    d.addCallback(lambda _: GObject.idle_add(callback, True))
    d.addCallback(w2.close)


def stop_sending(callback):
    global w2
    if w2 is not None:
        w2.close()

    GObject.idle_add(callback)


def start_receive(callback1, callback2):
    global w1
    w1 = wormhole(u"wormgui", RENDEZVOUS_RELAY, reactor)

    d = w1.get_code()
    d.addCallback(lambda c: _got_code(c, callback1))
    d.addCallback(lambda _: w1.get())
    d.addCallback(lambda m: _got_message(m, callback2))
    d.addCallback(w1.close)


def _got_code(code, callback):
    global w1
    logging.info("Invitation Code:", code)
    GObject.idle_add(callback, code)
    return w1.send(b"outbound data")


def _got_message(message, callback):
    logging.info("Message received:", message)
    GObject.idle_add(callback, message)


def stop_receiving(callback):
    global w1
    if w1 is not None:
        w1.close()

    GObject.idle_add(callback)
