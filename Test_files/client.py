#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

if __name__ == "__main__":
    sock = socket.socket()
    sock.connect(('localhost', 9090))
    sock.send('hello, world!'.encode())

    data = sock.recv(1024)
    sock.close()

    print(data)