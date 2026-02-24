from easysnmp import Session
from easysnmp import snmp_get
import json
import time
import matplotlib.pyplot as plt

def save_JSON():

    routers = ["10.0.0.2", "10.0.1.9", "10.0.1.5", "10.0.1.10", "10.0.2.1"]

    community = "password"

    output = {}

    for router in routers:

        print("Connecting to: ", router)

        try:
            session = Session(hostname=router, community = community, version = 2)
            hostname = session.get('.1.3.6.1.2.1.1.5.0').value
            if_desc = session.walk('.1.3.6.1.2.1.2.2.1.2')
            if_status = session.walk('.1.3.6.1.2.1.2.2.1.8')
            if_address = session.walk('.1.3.6.1.2.1.4.20.1.1')

            output[hostname] = {}

            for i in range(len(if_desc)):
                int_name = if_desc[i].value
                int_status = if_status[i].value
                try:
                    ipv4_address = if_address[i].value
                except:
                    ipv4_address = "unassigned"

                output[hostname][int_name] = {
                    "Status" : int_status,
                    "IPv4" : ipv4_address,
                }
            print("Finished Fetching from: ", hostname)
        except:
            print("error!")

    try:
        with open("snmp.txt", "w") as file:
            json.dump(output, file, indent=4)
        print("Successfully saved the JSON file.")
    except:
        print("error!")

def fetch_CPU():
    router = "10.0.2.1"
    community = "password"
    CPU_values = []

    print("Connecting to: ", router)
    
    i = 0

    while(i < 12):
        try:
            result = snmp_get(".1.3.6.1.4.1.9.2.1.56.0", version = 2, community = community, hostname = router)
        except:
            print("Error Connecting")

        print(f"{router} || CPU usage is at {result.value}%")

        CPU_values.append(int(result.value))

        time.sleep(5)
        i = i+1
    
    x_values = [i * 5 for i in range(len(CPU_values))]

    print(x_values)
    print(CPU_values)

    plt.plot(x_values, CPU_values)
    plt.xlabel("Time in Seconds")
    plt.ylabel("CPU usage")
    plt.ylim(min(CPU_values)-1, max(CPU_values)+1)
    plt.title("CPU Usage over Time")
    plt.savefig('CPU_Chart.png')   

if __name__ == "__main__":
    fetch_CPU()
    # save_JSON()