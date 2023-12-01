import ipaddress
from ipaddress import IPv4Network
import os
from tqdm import tqdm

'''
This script has been added to and will be archived
problems
  Built for MAC-OS and was transistioned to use pythonping for OS flexibility
  No Multithreading
  /30 network problems 
  no DNS lookups

'''

network = input('input network prefix in CIDR notation: ')

prefix = ipaddress.IPv4Network(f'{network}')
sub_len = prefix.num_addresses - 1


    

def sweep(prefix, sub_len):
    for i in tqdm(prefix, total=sub_len):
        response = os.system('ping -c 1 -t 1  %s > /dev/null' %i)
        if response == 0:
            print('%s up' %i)
        else:
            pass
            #print('%s no response' %i)


if __name__ == '__main__':
    
    sweep(prefix, sub_len)
