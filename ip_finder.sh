#!/bin/bash
if [ -z "${IP_ADDRESS}" ]; then
    nmap $(ip -4 a | grep 'state UP' -A 2 | grep inet | awk '{print $2}') -T4 -Pn -p 1521 --max-rtt-timeout 400ms | grep '1521/tcp open' -B 4 | grep 'report for' | awk '{print $5}' > IP_ADDRESS.txt
else
    echo "${IP_ADDRESS}" > IP_ADDRESS.txt
fi
if [ -z "${ORACLE_SID}" ]; then
    nmap $(cat /home/oracle-monitor/IP_ADDRESS.txt) --script oracle-sid-brute | grep oracle-sid-brute -A 1 | grep _ | awk '{print $2}' > ORACLE_SID.txt
else
    echo "${ORACLE_SID}" > ORACLE_SID.txt
fi