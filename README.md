Simple uni project.

A docker container based on jasonrivers/nagios providing pre-installed check_oracle_health plugin.
Should automatically discover target IP address and DB SID when ran (might take some time),
otherwise set IP_ADDRESS and ORACLE_SID when running image.

Very much not-elegant, and very much NOT for production.