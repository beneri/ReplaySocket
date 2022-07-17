from scapy.all import *
from timeit import default_timer as timer

class ReplaySocket:
    # conversation_key is (ip_src, port_src, ip_dst, port_dst)
    def __init__(self, pcap_file, conversation_key, speedup=1):
        # Increasing time_speedup will allow recv to fetch the data eariler
        self.time_speedup = speedup
        self.min_packet_time = 0

        self.string_buffer = b''
        # The index tracks how many bytes we have already returned
        self.string_buffer_index = 0

        # For some polling methods a socket.timeout is the correct
        # action for an empty response
        self.timeout_on_empty = False

        packets = rdpcap(pcap_file)
        self.socket_start_time = packets[0].time
        self.socket_last_time = packets[-1].time

        # Iterate through every packet and save the ones 
        # with matching conversation key (ip, port)
        self.time_packets = [(packet.time, packet[TCP].payload) 
                             for packet in packets 
                             if self.valid_packet(packet, conversation_key)]

        self.real_start_time = timer()

    def valid_packet(self, packet, conversation_key):
        # Checks if a packet is TCP and matches the conversation key
        if not TCP in packet:
          return False

        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        tcp = packet[TCP]
        port_src = tcp.sport
        port_dst = tcp.dport

        return (ip_src, port_src, ip_dst, port_dst) == conversation_key 

    def recv_time(self, size, time_since_start):
        # max_packet_time is the latest packet we can send back
        # based on the time_since_start
        max_packet_time = self.socket_start_time + time_since_start
        if max_packet_time > self.socket_last_time:
            print("No more data, ever")
            raise NameError('No more data')

        window = (self.min_packet_time, max_packet_time)
        packets_to_send = [p for (t,p) in self.time_packets 
                           if t > self.min_packet_time and t < max_packet_time]

        # For each packet in the window time frame, 
        # add the bytes of the packet to a string buffer
        for p in packets_to_send:
            self.string_buffer += bytes(p)

        # Update the earliest packet we can send back
        self.min_packet_time = max_packet_time

        # Ensure we do not add more data than specified by recv()
        if self.string_buffer_index+size > len(self.string_buffer):
            size = len(self.string_buffer) - self.string_buffer_index
            if self.timeout_on_empty and size < 1:
                raise socket.timeout

        # Extract the <size> bytes from the buffer
        data_start = self.string_buffer_index
        data_end = data_start + size
        data_to_return = self.string_buffer[data_start:data_end]
        self.string_buffer_index += size
        return data_to_return


    def recv(self, size):
        # This is called by the program using the socket. 
        # Internally, we use recv_time where we specify how much time 
        # has passed. 

        time_since_start = (timer() - self.real_start_time)*self.time_speedup
        return self.recv_time(size, time_since_start)

