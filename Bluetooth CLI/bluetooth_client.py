import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--message", type=str, help="message to send")
args = parser.parse_args()

server_mac = "5C:C5:D4:27:C7:F1"
port = 3  # Server and client must choose the same port
size = 1024
with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as s:
    s.connect((server_mac, port))
    if args.message:
        s.send(bytes(args.message, "UTF-8"))
    else:
        s.send(b"hello")
    data = s.recv(size)
    print("Echo received", data)
