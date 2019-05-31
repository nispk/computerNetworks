
import socket
import subprocess,os

command = "python task4b.py | & tee -a task4b_output.txt"

s=subprocess.call([command],shell = True)
print(s)

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8880        # Port to listen on (non-privileged ports are > 1023)

command = 'gnome-terminal --command="python echo-client.py"'
sub = subprocess.Popen([command], shell = True, preexec_fn=os.setsid)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(1)

while True:
	conn,addr = s.accept()
	print('Connected by', addr, conn)
        out_file = "task4b_output.txt"
        with open(out_file, 'rb') as f:
        	conn.send(f.read(1024))
        
   
