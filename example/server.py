# Based on example from: https://realpython.com/python-sockets/#echo-server
import socket
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 1234 # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")

        # Send A,B,C,D,E with 1 second pauses
        for i in range(5): 
          print("Sending ", i)
          conn.sendall(bytes([65+i]))
          print("Waiting 1 sec...")
          time.sleep(1)

        # Send . every 0.1 second
        for i in range(10): 
          print("Sending .")
          conn.sendall(bytes([ord('.')]))
          print("Waiting 0.1 sec...")
          time.sleep(0.1)

        # Send 1000 bytes to test recv(size)
        print("Waiting 1 sec")
        time.sleep(1)
        print("Sending 1000 bytes")
        conn.sendall(bytes([ord('A')]*1000))

        print("Waiting 1 sec")
        time.sleep(1)

        conn.close()


