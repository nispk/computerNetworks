
import socket,subprocess,os

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8888        # Port to listen on (non-privileged ports are > 1023)

command = 'gnome-terminal --command="python echo-client.py"'
sub = subprocess.Popen([command], shell = True, preexec_fn=os.setsid)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen(1)

while True:
	conn,addr = s.accept()
	print('Connected by', addr, conn)
        out_file = "Practise/task3b_output"
        err_file =  "Practise/task3b_error"
        task3bop = open(out_file, 'r')
        task3ber = open(err_file, 'r')
        conn.sendall(task3bop)
        conn.sendall(task3ber)
        #data = conn.recv(1024)
	#print ('received data is',data)
	#if not data:
      		#break
	#conn.sendall(data)
