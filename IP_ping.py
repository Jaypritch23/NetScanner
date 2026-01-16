#Ping all devices within a /24 subnet and return all ip addresses that send an echo reply

import subprocess
import threading

def scan(address: str):
    """Ping 1 packet address, wait 1ms for response. Discards output."""
    
    subprocess.run(
        ['ping', '-c', '1', '-W', '1', address],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def ping():
    """Using getifaddr, obtain private ip address. Ping all 254 addresses on separate threads."""
    try:
        # subprocess.check_output returns the ip as bytes, .decode decodes the bytes, strip removes ' '
        returned_address =  subprocess.check_output(['ipconfig', 'getifaddr', 'en0']).decode().strip()
        user_ip4_address = str(returned_address)
    except subprocess.CalledProcessError:
        print("Failed to get IP address. Are you on macOS and is en0 active?")


    private_address = []
    counter = 0


    #loop to get the network portion 
    for character in user_ip4_address:
        if counter == 10:
            break
        private_address.append(character) 
        counter += 1

    router_ip_address = ''.join(private_address)

    ip_address = [f"{router_ip_address}{i}" for i in range(1, 255)]

    threads = []
    for address in ip_address:
        t = threading.Thread(target=scan, args=(address,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()


