import os, sys, socket, platform, subprocess

from bin.socket_msg import socket_send_msg, socket_receive_msg


command = 'lxterminal --command="python client.py"'

ip="127.0.0.1"
port = 8888


sub = subprocess.Popen([command], shell = True,preexec_fn=os.setsid)
sub = os.getpgid(sub.pid)
print sub
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((ip,port))
soc.listen(5)
server_socket, addr = soc.accept()

while True:
    data_out = socket_send_msg(soc)
    data_in = socket_receive_msg(soc)

print "the received data from client is",data_in

