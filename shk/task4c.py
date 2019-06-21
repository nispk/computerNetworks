#!/usr/bin/env python
import argparse
import numpy as np
import random
import sys
import os , subprocess , socket
from pathlib import Path


HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8881        # Port to listen on (non-privileged ports are > 1023)

command = 'gnome-terminal --command="python echo-client.py"'
sub = subprocess.Popen([command], shell = True, preexec_fn=os.setsid)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(1)

while True:
	conn,addr = s.accept()
	print('Connected by', addr, conn)
        out_file = '/home/asn/asn_daemon/system/2/out_file'
        err_file = '/home/asn/asn_daemon/system/2/err_file'
        with open(out_file, 'rb') as f:
        	conn.send(f.read(1024))
        with open(err_file, 'rb') as f:
        	conn.send(f.read(1024))

