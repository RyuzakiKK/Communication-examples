from bluetooth import *
import threading
import gi
import logging
gi.require_version('Gtk', '3.0')
from gi.repository import GObject


logger = logging.getLogger(__name__)
server_socket = None


def discover(callback):
    logging.info("performing inquiry...")
    t = threading.Thread(target=_start_discover, args=[callback, ])
    t.start()


def _start_discover(callback):
    nearby_devices = discover_devices(
         duration=5, lookup_names=True, flush_cache=True, lookup_class=False)
    logging.info("found %d devices" % len(nearby_devices))
    for name, address in nearby_devices:
        logging.debug("{0} - {1}".format(address, name))

    GObject.idle_add(callback, nearby_devices)


def send(mac, port, message, callback):
    logging.info("Sending a message")
    t = threading.Thread(target=_start_send, args=[mac, port, message, callback])
    t.start()


def _start_send(mac, port, message, callback):
    completed = True
    client_socket = BluetoothSocket(RFCOMM)
    try:
        client_socket.connect((mac, port))
        client_socket.send(message)
        logging.info("Send completed")
        client_socket.close()
    except btcommon.BluetoothError:
        logging.info("Error sending the message")
        completed = False

    GObject.idle_add(callback, completed)


def start_receive(port, size, callback):
    logging.info("Listening for external messages")
    t = threading.Thread(target=_receive_accept, args=[port, size, callback])
    t.start()


def _receive_accept(port, size, callback):
    global server_socket
    if server_socket is None:
        server_socket = BluetoothSocket(RFCOMM)
        server_socket.bind(("", port))
        backlog = 1  # Number of unaccepted connections that the system will allow before refusing new connections
        server_socket.listen(backlog)
    client_socket, address = server_socket.accept()
    data = client_socket.recv(size)
    logging.debug("received [%s]" % data)
    client_socket.close()
    server_socket.close()

    GObject.idle_add(callback, data)


def stop_receive():
    global server_socket
    if server_socket is not None:
        server_socket.close()
