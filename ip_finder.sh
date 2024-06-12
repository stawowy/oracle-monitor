#!/bin/bash
# Script for finding and storing target DB information, if fails, deal with it, set the files yourself
nmap $(echo ${SUBNET_ADDR}) -T4 -Pn -p 1521 --max-rtt-timeout 400ms | grep '1521/tcp open' -B 4 | grep 'report for' | awk '{print $5}' > /home/oracle-monitor/IP_ADDRESS.txt
nmap $(cat /home/oracle-monitor/IP_ADDRESS.txt) --script oracle-sid-brute | grep oracle-sid-brute -A 1 | grep _ | awk '{print $2}' > /home/oracle-monitor/ORACLE_SID.txt