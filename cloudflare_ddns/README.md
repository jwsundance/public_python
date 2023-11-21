#  Public IP address check and API PATCH update to Cloudflare DNS 
# I created this to check for my public IP address and compare it to the current DNS entry I had configured thorugh cloudflare. 

#I setup a virtual environment and used a cron to run the script inside of the venv every 30 minutes and write the printed outputs to a txt #file in the same directoy as the script. 

###below is the crontab line to run the script###

#30 * * * * /opt/01_projects/01_ddns/bin/python3 /opt/01_projects/01_ddns/01_pub_ip/pub_ip.py >> #/opt/01_projects/01_ddns/01_pub_ip/pub_ip_log.txt 2>&1

#the first section of the cron outlines the venv to run the script from. The third section appends each output line from the script to the file I am using for logging. 


This is just how I did it...not sure if any of this is right but I hope it helps someone.

