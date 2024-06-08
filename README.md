Simple uni project.

A docker container based on jasonrivers/nagios providing pre-installed check_oracle_health plugin, and nmap with a vulners plugin to chech basic vulnerabilities.
Should automatically discover target IP address and DB SID when ran (might take some time),
otherwise set IP_ADDRESS and ORACLE_SID when running image.

After regular docker run startup navigate to /home/oracle-monitor and run 'python3 init.py'.

Not-elegant, and very much NOT for production.