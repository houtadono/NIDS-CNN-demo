from scapy.all import *

protocol_map = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
service_map = {
    20: 'ftp_data', 42: 'name', 57: 'mtp', 23: 'telnet', 79: 'finger', 80: 'http', 95: 'supdup',
    137: 'netbios_ns', 123: 'ntp_u', 69: 'tftp_u',
    117: 'uucp_path', 210: 'Z39_50', 25: 'smtp', 105: 'csnet_ns', 540: 'uucp', 138: 'netbios_dgm', 53: 'domain',
    21: 'ftp', 179: 'bgp', 389: 'ldap', 70: 'gopher', 175: 'vmnet', 11: 'systat', 443: 'http_443', 520: 'efs',
    43: 'whois', 143: 'imap4', 102: 'iso_tsap', 7: 'echo', 543: 'klogin',
    87: 'link', 111: 'sunrpc', 513: 'login', 544: 'kshell', 150: 'sql_net', 37: 'time',
    101: 'hostnames', 512: 'exec', 9: 'discard', 119: 'nntp', 22: 'ssh', 13: 'daytime', 514: 'shell',
    15: 'netstat', 110: 'pop_3', 194: 'IRC', 109: 'pop_2', 515: 'printer', 139: 'netbios_ssn', 6000: 'X11',
    8001: 'http_8001', 2784: 'http_2784'  # nếu k có thì là other
}


def categorize_scapy_flags(flags):
    if "S" in flags and "F" not in flags:  # SYN
        return 'SF'
    elif not flags:  # NULL
        return 'S0'
    elif "R" in flags:  # RST
        return 'RSTR'
    elif "S" in flags and "H" in flags:  # SYN-ACK (half-open)
        return 'SH'
    elif "R" in flags and "A" in flags:  # RST-ACK
        return 'RSTR'
    elif "R" in flags:  # RST (reset)
        return 'RSTO'
    elif "S" in flags and "F" in flags:  # SYN/FIN
        return 'S1'
    elif "S" in flags and "F" in flags and "P" in flags:  # SYN/PSH/FIN
        return 'S2'
    elif "S" in flags and "F" in flags and "A" in flags:  # SYN/ACK/FIN
        return 'S3'
    else:
        return 'OTH'


def extract_features(packet):
    features = {}
    try:
        features['duration'] = packet.time  # Duration of the connection
        features['protocol_type'] = protocol_map[
            packet[IP].proto]  # map protocol, nếu không có protocol trong map thì return None
        features['service'] = service_map.get(packet[TCP].dport, 'other')
        features['flag'] = categorize_scapy_flags(packet[TCP].flags)

        features['src_bytes'] = len(packet[
                                        TCP].payload) if TCP in packet and Raw in packet else 0  # Number of data bytes transferred from source to destination
        features['dst_bytes'] = len(packet[
                                        TCP].payload) if TCP in packet and Raw in packet else 0  # Number of data bytes transferred from destination to source
        features['land'] = 1 if packet[IP].src == packet[IP].dst and packet[TCP].sport == packet[
            TCP].dport else 0  # Land
        features['wrong_fragment'] = packet[IP].frag  # Total number of wrong fragments
        features['urgent'] = packet[TCP].urgptr  # Number of urgent packets

        features['hot'] = 0  # Number of "hot" indicators
        features['num_failed_logins'] = 0  # Count of failed login attempts
        features['logged_in'] = 0  # Login status
        features['num_compromised'] = 0  # Number of "compromised" conditions
        features['root_shell'] = 0  # Root shell status
        features['su_attempted'] = 0  # Su attempted status
        features['num_root'] = 0  # Number of root accesses
        features['num_file_creations'] = 0  # Number of file creation operations
        features['num_shells'] = 0  # Number of shell prompts
        features['num_access_files'] = 0  # Number of operations on access control files
        features['num_outbound_cmds'] = 0  # Number of outbound commands
        features['is_host_login'] = 0  # Host login status
        features['is_guest_login'] = 0  # Guest login status
        features['count'] = 0  # Number of connections to the same destination host
        features['srv_count'] = 0  # Number of connections to the same service
        features['serror_rate'] = 0.0  # Serror rate
        features['srv_serror_rate'] = 0.0  # Srv serror rate
        features['rerror_rate'] = 0.0  # Rerror rate
        features['srv_rerror_rate'] = 0.0  # Srv rerror rate
        features['same_srv_rate'] = 0.0  # Same srv rate
        features['diff_srv_rate'] = 0.0  # Diff srv rate
        features['srv_diff_host_rate'] = 0.0  # Srv diff host rate
        features['dst_host_count'] = 0  # Dst host count
        features['dst_host_srv_count'] = 0  # Dst host srv count
        features['dst_host_same_srv_rate'] = 0.0  # Dst host same srv rate
        features['dst_host_diff_srv_rate'] = 0.0  # Dst host diff srv rate
        features['dst_host_same_src_port_rate'] = 0.0  # Dst host same src port rate
        features['dst_host_srv_diff_host_rate'] = 0.0  # Dst host srv diff host rate
        features['dst_host_serror_rate'] = 0.0  # Dst host serror rate
        features['dst_host_srv_serror_rate'] = 0.0  # Dst host srv serror rate
        features['dst_host_rerror_rate'] = 0.0  # Dst host rerror rate
        features['dst_host_srv_rerror_rate'] = 0.0  # Dst host srv rerror rate
        return features
    except:
        return None
    pass


packet = IP() / TCP(dport=80)
extracted_features = extract_features(packet)
print(extracted_features)
