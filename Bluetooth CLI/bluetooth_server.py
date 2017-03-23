import socket

host_mac = "5C:C5:D4:27:C7:F1"
port = 3  # Server and client must choose the same port
backlog = 1  # Number of unaccepted connections that the system will allow before refusing new connections
size = 1024

with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as s:
    s.bind((host_mac, port))
    s.listen(backlog)
    conn, addr = s.accept()
    with conn:
        data = conn.recv(size)
        conn.send(data)
        print(data)
