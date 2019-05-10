#!/usr/bin/env python
import argparse
import numpy as np
import sys,os
import socket,subprocess


def parse_arguments():
    parser = argparse.ArgumentParser(description='arguments')

    parser.add_argument("--inputs", "-i",
                            action="append")

    return parser.parse_args()

args = parse_arguments()
inputs = [os.fdopen(int(args.inputs[0]), 'rb')]



x = np.fromfile(inputs[0],dtype=np.float16,count=5)

print x

w = np.mean(x)
print w

#print 'task2b output:'+'data received :'+ str(z)
sys.stdout.flush()

'''
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 5353        # Port to listen on (non-privileged ports are > 1023)

command = 'lxterminal --command="python echo-client.py"'
sub = subprocess.Popen([command], shell = True, preexec_fn=os.setsid)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

while True:
	conn, addr = s.accept()
	print('Connected by', addr)
	data = conn.recv(1024)
	conn.sendall(w)
	if not data:
      		break

'''
	
