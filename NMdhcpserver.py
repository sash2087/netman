
import json
import NMtcpdump
from netmiko import(
    ConnectHandler,
    NetmikoTimeoutException,
    NetMikoAuthenticationException,
)
import re
import NMtcpdump

if __name__ == "__main__":

    # Task 1: SSH into R4 using IPv6 address. Retreive R5's IPv6 Address.

    print("SSHing into R4.")

    R4 = {
    "device_type" : "cisco_ios_ssh",
    "host": "2001:db8:c2:d2::1",
    "username": "admin",
    "password": "password",
    "secret": "password"
    }

    commands = ["do ping 2001:db8:C2:D1:c805:31FF:FEFC:0","do show ipv6 neighbors"]

    with ConnectHandler(**R4) as conf:
        if not conf.check_enable_mode():
            conf.enable()
        output = conf.send_config_set(commands)

    print("Grabbing R5's IPv6 Address")
    print(output)
    
    p = r"2001:DB8:C2:D1:C805(:[0-9A-F]{1,4}){1,7}"

    R5_ip_search = re.search(p, output, re.IGNORECASE)
    R5_ip = R5_ip_search.group()

    # Task 2: SSH into R5, and configure DHCP on it.
    print("R5 Address: ", R5_ip)
    print("Configuring DHCP in R5.")

    R5 = {
    "device_type" : "cisco_ios_ssh",
    "host": R5_ip,
    "username": "admin",
    "password": "password",
    "secret": "password"
    }

    ip = NMtcpdump.filter()

    R2 = ip[0]
    R2 = "01"+ R2.replace(":","")
    R3 = ip[1]
    R3 = "01"+ R3.replace(":","")

    print(R2)
    print(R3)
    commands_1 = ["ip dhcp excluded-address 10.0.1.9 10.0.1.10", "ip dhcp pool static1" , "host 10.0.1.9 255.255.255.0", "client-identifier " + R2]
    commands_2 = ["ip dhcp pool static2", "host 10.0.1.10 255.255.255.0", "client-identifier " + R3]
    commands_3 = ["ip dhcp pool Midterm", "network 10.0.1.0 255.255.255.0", "default-router 10.0.1.5"]
 
    try:
        for commands in [commands_1, commands_2, commands_3]:
            with ConnectHandler(**R5) as router:
                router.enable()
                output = router.send_config_set(commands)
                print(output)
    except (NetmikoTimeoutException, NetMikoAuthenticationException) as error:
        print(error)

