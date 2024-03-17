from scapy.all import *

# Dictionary to store packets of each connection
connections = {}

def process_packet(packet):
    if IP in packet:
        if packet.haslayer(ICMP):  # Check if packet contains ICMP layer
            connection_id = (packet[IP].src, 'ICMP', packet[IP].dst)
        elif TCP in packet:  # Check if packet contains TCP layer
            connection_id = (packet[IP].src, packet[TCP].sport, packet[IP].dst, packet[TCP].dport)
        elif UDP in packet:  # Check if packet contains UDP layer
            connection_id = (packet[IP].src, packet[UDP].sport, packet[IP].dst, packet[UDP].dport)
        else:
            return

        if connection_id not in connections:
            connections[connection_id] = {'start_time': packet.time, 'end_time': None, 'packets': []}
        connections[connection_id]['packets'].append(packet)

        if packet.haslayer(ICMP) and packet[ICMP].type in (0, 8):  # ICMP echo request/reply
            connections[connection_id]['end_time'] = packet.time

            # Calculate traffic volume
            src_bytes = sum(len(p) for p in connections[connection_id]['packets'] if p[IP].src == connection_id[0])
            dst_bytes = sum(len(p) for p in connections[connection_id]['packets'] if p[IP].dst == connection_id[2])

            # Calculate duration
            duration = connections[connection_id]['end_time'] - connections[connection_id]['start_time']

            # Print traffic volume and duration
            print(f"Connection {connection_id}:")
            print(f"  - Source bytes: {src_bytes}")
            print(f"  - Destination bytes: {dst_bytes}")
            print(f"  - Duration: {duration} seconds")
            print()

        if TCP in packet and (packet[TCP].flags & 0x01 or packet[TCP].flags & 0x04):  # FIN or RST flag is set
            # This is the end of the connection
            connections[connection_id]['end_time'] = packet.time

            # Calculate traffic volume
            src_bytes = sum(len(p) for p in connections[connection_id]['packets'] if p[IP].src == connection_id[0])
            dst_bytes = sum(len(p) for p in connections[connection_id]['packets'] if p[IP].dst == connection_id[2])
            duration = connections[connection_id]['end_time'] - connections[connection_id]['start_time']

            # Print traffic volume
            print(f"Connection {connection_id}:")
            print(f"  - Source bytes: {src_bytes}")
            print(f"  - Destination bytes: {dst_bytes}")
            print(f"  - Duration: {duration} seconds")
            print()



# Open pcap file and process packets
pcap_file = "../b.pcap"
packets = rdpcap(pcap_file)
for packet in packets:
    process_packet(packet)
