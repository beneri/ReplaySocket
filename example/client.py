# Based on example from: https://realpython.com/python-sockets/#echo-server
import socket
from timeit import default_timer as timer



HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1234 # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

start_time = timer()
while True:
  data = s.recv(256)
  if data:
    elapsed = timer() - start_time
    print("["+str(elapsed)+"] Got data: ", data)


