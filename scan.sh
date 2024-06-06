#!/bin/bash
echo 'Vulnerability scan:\n' > /home/reports/report.txt
nmap -sV --script nmap-vulners/ $(cat IP_ADDRESS.txt) >> /home/reports/report.txt
echo 'DB performance/stats scan:\n' >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(cat IP_ADDRESS.txt):1521/$(cat ORACLE_SID.txt) --username=nagios --password=nagios --mode tnsping >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(cat IP_ADDRESS.txt):1521/$(cat ORACLE_SID.txt) --username=nagios --password=nagios --mode connection-time >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(cat IP_ADDRESS.txt):1521/$(cat ORACLE_SID.txt) --username=nagios --password=nagios --mode session-usage >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(cat IP_ADDRESS.txt):1521/$(cat ORACLE_SID.txt) --username=nagios --password=nagios --mode process-usage >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(cat IP_ADDRESS.txt):1521/$(cat ORACLE_SID.txt) --username=nagios --password=nagios --mode rman-backup-problems >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(cat IP_ADDRESS.txt):1521/$(cat ORACLE_SID.txt) --username=nagios --password=nagios --mode sga-data-buffer-hit-ratio >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(cat IP_ADDRESS.txt):1521/$(cat ORACLE_SID.txt) --username=nagios --password=nagios --mode sga-shared-pool-free >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(cat IP_ADDRESS.txt):1521/$(cat ORACLE_SID.txt) --username=nagios --password=nagios --mode tablespace-usage >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(cat IP_ADDRESS.txt):1521/$(cat ORACLE_SID.txt) --username=nagios --password=nagios --mode tablespace-fragmentation >> /home/reports/report.txt
/usr/local/nagios/libexec/check_oracle_health --connect=$(cat IP_ADDRESS.txt):1521/$(cat ORACLE_SID.txt) --username=nagios --password=nagios --mode switch-interval >> /home/reports/report.txt