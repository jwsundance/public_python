#  Simple ping sweep in python that takes in a prefix in CIDR and pings each IP in the prefix and prints an output if the IP responds.


#The progress bar will act as a debugging tool. The total number of addresses (-1) will be 100% of the status bar. i.e. if you have a /24 it calculates the total number of addresses (255) and subtracts (1) to make (254). Each IP is one "tick" of the status bar. (if the bar is moving the script is running and getting results. 
