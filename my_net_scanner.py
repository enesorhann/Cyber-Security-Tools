import scapy.all as scapy
import optparse
#1)arp_request
#2)broadcast
#3)response

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i","--ipaddress",dest = "ip_address",help = "Enter IP Address")

    (user_input,arguments) = parse_object.parse_args()
    if not user_input.ip_address:
        print("Enter IP Address")
    return user_input

def scan_my_Network(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    #scapy.ls(scapy.ARP())
    broadcast_packet = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    #scapy.ls(scapy.Ether())
    combined_packet = broadcast_packet/arp_request_packet   #Sağdaki iki paketii soldaki tek pakette birleştir
    #Birleştirdikten sonra geriye yollamak ve birleştirmek kalıyor.
    (answered_list,unanswered_list) = scapy.srp(combined_packet,timeout=1)   #Cevap verilmeyince beklemeye devam et demektir.
    answered_list.summary()

user_ip_address = get_user_input()
scan_my_Network(user_ip_address.ip_address)
