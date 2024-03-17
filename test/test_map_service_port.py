service_map = {
    20: 'ftp_data', 42: 'name', 57: 'mtp', 23: 'telnet', 79: 'finger', 80:'http', 95: 'supdup',
    137: 'netbios_ns', 123: 'ntp_u', 69: 'tftp_u',
    117: 'uucp_path', 210: 'Z39_50', 25: 'smtp', 105: 'csnet_ns', 540: 'uucp', 138: 'netbios_dgm', 53: 'domain',
    21: 'ftp', 179: 'bgp', 389: 'ldap', 70: 'gopher', 175: 'vmnet', 11: 'systat', 443: 'http_443', 520: 'efs',
    43: 'whois', 143: 'imap4', 102: 'iso_tsap', 7: 'echo', 543: 'klogin',
    87: 'link', 111: 'sunrpc', 513: 'login', 544: 'kshell', 150: 'sql_net', 37: 'time',
    101: 'hostnames', 512: 'exec', 9: 'discard', 119: 'nntp', 22: 'ssh', 13: 'daytime', 514: 'shell',
    15: 'netstat', 110: 'pop_3', 194: 'IRC', 109: 'pop_2', 515: 'printer', 139: 'netbios_ssn', 6000: 'X11',
    8001: 'http_8001', 2784: 'http_2784'
}

full = ['ftp_data', 'other', 'private', 'http', 'remote_job', 'name',
       'netbios_ns', 'eco_i', 'mtp', 'telnet', 'finger', 'domain_u',
       'supdup', 'uucp_path', 'Z39_50', 'smtp', 'csnet_ns', 'uucp',
       'netbios_dgm', 'urp_i', 'auth', 'domain', 'ftp', 'bgp', 'ldap',
       'ecr_i', 'gopher', 'vmnet', 'systat', 'http_443', 'efs', 'whois',
       'imap4', 'iso_tsap', 'echo', 'klogin', 'link', 'sunrpc', 'login',
       'kshell', 'sql_net', 'time', 'hostnames', 'exec', 'ntp_u',
       'discard', 'nntp', 'courier', 'ctf', 'ssh', 'daytime', 'shell',
       'netstat', 'pop_3', 'nnsp', 'IRC', 'pop_2', 'printer', 'tim_i',
       'pm_dump', 'red_i', 'netbios_ssn', 'rje', 'X11', 'urh_i',
       'http_8001', 'aol', 'http_2784', 'tftp_u', 'harvest'
     ]
unknown = ['other', 'private', 'remote_job', 'eco_i', 'urp_i', 'auth', 'ecr_i', 'courier', 'ctf', 'tim_i', 'pm_dump', 'red_i', 'rje', 'urh_i', 'aol', 'harvest', 'domain_u', 'nnsp']

print(len(b))
print(len(service_map), len(full))

c = []
for i in service_map.keys():
    c.append(service_map[i])

services_without_port = [service for service in full if service not in c]

print(services_without_port)

print([ i for i in services_without_port if i not in b])