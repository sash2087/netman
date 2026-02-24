from scapy.all import *

def filter():

    packets = rdpcap("midterm_capt.pcap")

    return_value = []

    for packet in packets:
        if Ether in packet and IPv6 in packet and ICMPv6EchoRequest in packet:
            if ICMPv6EchoRequest in packet:
                if slaac_conversion(packet[IPv6].src) not in return_value:
                    return_value.append(slaac_conversion(packet[IPv6].src))

    return return_value

def slaac_conversion(ipv6):

    split_ip = ipv6.split(":")
    last_four = split_ip[-4:]

    mac = []

    # fill out the missing digits with 0.
    # take the last 4 groups of the ip address and normalize the length.
    for each in last_four:
        if len(each) == 1:
            couple = "000" + each
            mac.append(couple[:2])
            mac.append(couple[-2:])
        elif len(each) == 2:
            couple = "00" + each
            mac.append(couple[:2])
            mac.append(couple[-2:])
        elif len(each) == 3:
            couple = "0" + each
            mac.append(couple[:2])
            mac.append(couple[-2:])
        else:
            couple = each
            mac.append(couple[:2])
            mac.append(couple[-2:])

    #turn first couple into hex and mask the 7th bit:
    hex = int(mac[0], 16)
    flipped_1 = hex^2
    flipped_2 = "%02x" % flipped_1
    mac[0] = flipped_2

    #remove ff and fe from the middle.
    mac.pop(4)
    mac.pop(3)

    final_mac = ":".join(mac)
    return final_mac

if __name__ == "__main__":
    print(filter())
