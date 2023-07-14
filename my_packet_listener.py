import scapy.all as scapy
from scapy.layers import http

def analyze_packets(packet):
    #packet.show()
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)

def listen_packets(interface):
    scapy.sniff(iface=interface,store=False,prn=analyze_packets)
    #prn = Callback Function

listen_packets("eth0")
