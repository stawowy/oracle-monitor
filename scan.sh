echo 'Vulnerability scan:\n' > /home/reports/report.txt
nmap -sV --script nmap-vulners/ $(echo $IP_ADDRESS) >> /home/reports/report.txt
echo 'DB performance/stats scan:\n' >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(echo $IP_ADDRESS):1521/$(echo $ORACLE_SID) --username=nagios --password=nagios --mode tnsping >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(echo $IP_ADDRESS):1521/$(echo $ORACLE_SID) --username=nagios --password=nagios --mode connection-time >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(echo $IP_ADDRESS):1521/$(echo $ORACLE_SID) --username=nagios --password=nagios --mode session-usage >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(echo $IP_ADDRESS):1521/$(echo $ORACLE_SID) --username=nagios --password=nagios --mode process-usage >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(echo $IP_ADDRESS):1521/$(echo $ORACLE_SID) --username=nagios --password=nagios --mode rman-backup-problems >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(echo $IP_ADDRESS):1521/$(echo $ORACLE_SID) --username=nagios --password=nagios --mode sga-data-buffer-hit-ratio >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(echo $IP_ADDRESS):1521/$(echo $ORACLE_SID) --username=nagios --password=nagios --mode sga-shared-pool-free >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(echo $IP_ADDRESS):1521/$(echo $ORACLE_SID) --username=nagios --password=nagios --mode tablespace-usage >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(echo $IP_ADDRESS):1521/$(echo $ORACLE_SID) --username=nagios --password=nagios --mode tablespace-fragmentation >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(echo $IP_ADDRESS):1521/$(echo $ORACLE_SID) --username=nagios --password=nagios --mode switch-interval >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(echo $IP_ADDRESS):1521/$(echo $ORACLE_SID) --username=nagios --password=nagios --mode list-sysstats >> /home/reports/report.txt