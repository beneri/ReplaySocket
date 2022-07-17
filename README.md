# ReplaySocket
Replay traffic from PCAP files with python sockets. 

Multiple times when working on security projects and CTF challenges I've found the
need to replay network traffic on a client. 

This project can be useful if you have access to 
both network traffic (in the form of a PCAP file) 
and python client code that use `socket`s. 

It is also possible speed up or slow down the traffic. 


## Example

The following is a simple example of a client that uses a socket to 
receive data from a server. 

```
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

start_time = timer()
while True:
  data = s.recv(256)
  if data:
    elapsed = timer() - start_time
    print("["+str(elapsed)+"] Got data: ", data)
```
After a conversation between the client and server, assume the data
is stored in a PCAP file, e.g. _traffic.pcap_. 
Then, if we want to replay this conversation in real-time, we simply 
make the following minor update to the client code. 

```
speed = 1
s = ReplaySocket("traffic.pcap", ("127.0.0.1", 1234, "127.0.0.1", 53066), speed)


start_time = timer()
while True:
  data = s.recv(256)
  if data:
    elapsed = timer() - start_time
    print("["+str(elapsed)+"] Got data: ", data)
```


