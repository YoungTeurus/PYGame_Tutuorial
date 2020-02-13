import socket

if __name__ == "__main__":
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(1)
    conn, addr = sock.accept()

    print('connected:', addr)

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        conn.send(data.upper().encode())

    conn.close()