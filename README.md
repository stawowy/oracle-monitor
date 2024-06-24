Uni project.

A docker container based on jasonrivers/nagios providing pre-installed check_oracle_health plugin, and nmap with a vulners plugin as a custom nagios plugin to check for basic DB vulnerabilities.
Should automatically discover target IP address and DB SID when ran (might take some time),
otherwise set IP_ADDRESS and ORACLE_SID when running image.

Assumes 192.168.x.0/24 subnet and generic ODB SID for simplicity. You can manually change the values of /home/oracle-monitorIP_ADDRESS and ORACLE_SID files.

Works with Gmail mails with app passwords as mail sender.

Not for production use.