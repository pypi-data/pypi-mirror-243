# cidrtip/cidr.py
import ipaddress

def cidr(cidr_input):
    ip_list = []
    network = ipaddress.IPv4Network(cidr_input, strict=False)
    for ip in network:
        ip_list.append(str(ip))
    return ip_list
