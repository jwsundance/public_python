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
    """Pings the host, resolves the hostname, then updates the address record
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
        hostname = socket.gethostbyaddr(host)[0]
    except Exception as e:
        hostname = None

    # Update results
    addresses[host].update({
        "PING_REPLY": ping_result,
        "DNS_NAME": hostname
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
    # Check how many threads have completed, and update the progress bar.
    while True:
        time.sleep(1)
        completed_count = 0
        for thread in threads:
            if thread._state == 'FINISHED':
                completed_count = completed_count + 1
        printProgressBar(completed_count, address_count, prefix="Pinging: ", suffix="Complete", length=50)
        if completed_count == address_count:
            break
    thread_pool.shutdown()

    print(f"{' '*120}", end="\r")
    print("Done attempting to ping IP addresses.")
    print("-"*78)
        

def printProgressBar(iteration: int, total: int , prefix: str = '',
                    suffix: str = '', decimals: int = 1, length: int = 100,
                    fill: str = '█', printEnd: str = "\r") -> None:
    """Prints a progress bar.

    Args:
        iteration (int): Current interation.
        total (int): Total possible iterations.
        prefix (str, optional): A string that is placed in front of the bar. Defaults to ''.
        suffix (str, optional): A string that is placed in front of the bar. Defaults to ''.
        decimals (int, optional): How precise the precentage shows. Defaults to 1.
        length (int, optional): How many characters long is the bar. Defaults to 100.
        fill (str, optional): What character is used to fill the bar. Defaults to '█'.
        printEnd (str, optional): What should be printed at each update. Defaults to "\r".

    Returns:
        None
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print(f"{' '*120}", end="\r")


def start_sweep() -> dict:
    """Pings all possible HOST addresses in a prefix.

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
            addresses.update({str(address): {"IPv4Address": address}})
    multithread_ping_ip(addresses=addresses)
    return addresses


if __name__ == '__main__':
    from pprint import pprint
    addresses = start_sweep()
    pprint(addresses, sort_dicts=False)
    input('Press ENTER to exit.')
