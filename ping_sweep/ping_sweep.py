"""
Run `start_sweep()` and it will ask for a prefix.  The script will then
do a ping sweep for all host IPs in that prefix, while also returning 
the hostname (if available) of the device with that IP.
"""

# Built-in Modules
import time
import socket
import ipaddress
import platform
import subprocess
import concurrent.futures
from pprint import pprint       #imported pprint here 20231202 JW

# Downloaded Modules
from tqdm import tqdm           # python -m pip install tqdm 20231202 JW

def ping(host: str, count: int = 4) -> bool:
    """Pings a host a returns if the ping was successful.

    Args:
        host (str): The IP address of the host.
        timeout (int, optional): Timeout of each ping, in seconds. Defaults to 1.
        count (int, optional): How many pings to try. Recommanded to do more than 1. Defaults to 4.

    Returns:
        bool: True if successful, False if not.
    """

    # modify the `ping` command depending on the operating system
    if platform.system().lower()=='windows':
        count_param = '-n'
    else:
        count_param = '-c'

    command = ['ping', count_param, str(count), host]
    proc = subprocess.Popen(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    
    while True:
        time.sleep(1)
        if proc.poll() is not None:
            break
        
    result =  proc.poll() == 0
    return result


def ping_and_update(addresses: dict, host: str) -> None:
    """
    Pings the host, resolves the hostname, then updates the address record
    in the provided `addresses` dictionary.

    Args:
        addresses (dict): Dictionary containing all the addresses as top-level keys.
        host (str): The specific IP address that is getting worked on.

    Returns:
        None
    """
    # Test ping to host address
    ping_result = ping(host)

    # Try DNS lookup to host address
    try:
        hostname = socket.getfqdn(host)#[0] #changed gethostbyaddr to getfqdn and have an output no matter what 20231202 JW
    except Exception as e:
        hostname = None
    #Update results
    addresses[host].update({
    "PING_REPLY": ping_result,
    "DNS_NAME": hostname ,
    })
        

def multithread_ping_ip(addresses: dict) -> None:
    """Loops through all the addresses in the provided dictionary, then starts
    a new thread to ping it and resolve the hostname via the IP.  Prints out
    status bar to show progress.

    Args:
        addresses (dict): Each top-level key name must be the IP address

    Returns:
        None
    """
    # Send each IP address through a `ping` command, and check if there is a reply.
    # The function will also add the results to the `addresses` dictionary
    address_count = len(addresses)
    print(f"Attempting to ping all {address_count} addresses to check for explicit network liveliness.")
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=15)
    threads = []
    for address in addresses:
        threads.append(thread_pool.submit(ping_and_update, addresses, address))
        thread_active = concurrent.futures.as_completed(fs=threads, timeout=None) #get count of threads and completed threading 
    for t in tqdm(thread_active, total=len(threads), mininterval=2): #implemented tqdm progress bare based off the completion of the active threads and total thread job count 20231202
        pass
    thread_pool.shutdown()

    #added some printing decorations to make visually appealing ;) 20231202 JW
    print("#"*89)
    print(f"{'_'*25}", "Done attempting to ping IP addresses", f"{'_'*25}")
    print("#"*89)


def start_sweep() -> dict:
    
    """
    Pings all possible HOST addresses in a prefix.

    Returns:
        dict: A dictionary containing all IPs as a top-level key.  Each key
            has a ping result, DNS hostname lookup, and IPv4Address objec
            for the associated IP address.
    """
    prefix = ipaddress.IPv4Network(input('input network prefix in CIDR notation: '))
    sub_len = prefix.num_addresses - 1
    addresses = {}
    for i, address in enumerate(prefix):
        if (i < sub_len and i > 0) or sub_len < 2:
            addresses.update({str(address): {'IPv4Address': address.compressed}}) #added compressed version of the returned address to clean up dictionary value 20231202 JW 
    multithread_ping_ip(addresses=addresses)
    return addresses

def print_dict(addresses: dict, **kwargs) -> None:
    '''
    split out pprint to function to allow for passing of **kwargs
    added **kwargs to fix issue not seeing values in values dictionary
    
    
    pprint added width=300 to print on one line 
    pprint added sort_dicts=True to put PING_REPLY at the end of the values dictionary
        

    Kwargs    
        addresses (dict): Each top-level key name must be the IP address
        IPv4Address (str): value is from address.compressed
        PING_REPLY (str): value is from pythonping -> will be changed to another utility
        DNS_NAME (str): value is from socket.getfqdn
        
    Returns:
        None #print function only
    
    20231202 JW
    '''
    pprint(addresses, width= 300, sort_dicts=True, **kwargs)
    
    
if __name__ == '__main__':
    addresses = start_sweep()
    print_dict(addresses)
