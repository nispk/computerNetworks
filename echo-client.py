#!/usr/bin/env python3

import socket
import numpy as np

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 8888        # The port used by the server


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
        data = s.recv(1024)
        print(data)
        
