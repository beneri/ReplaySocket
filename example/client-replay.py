# Based on example from: https://realpython.com/python-sockets/#echo-server
import socket
from timeit import default_timer as timer

from ReplaySocket import ReplaySocket 

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1234 # The port used by the server

s = ReplaySocket("traffic.pcap", ("127.0.0.1", 1234, "127.0.0.1", 53066), 2)


start_time = timer()
while True:
  data = s.recv(256)
  if data:
    elapsed = timer() - start_time
    print("["+str(elapsed)+"] Got data: ", data)


