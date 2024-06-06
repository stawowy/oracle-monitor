#!/bin/bash
if [ -z "${IP_ADDRESS}" ]; then
    export IP_ADDRESS=$(nmap $(ip -4 a | grep 'state UP' -A 2 | grep inet | awk '{print $2}') -T4 -Pn -p 1521 --max-rtt-timeout 400ms | grep '1521/tcp open' -B 4 | grep 'report for' | awk '{print $5}')
fi
if [ -z "${ORACLE_SID}" ]; then
    export ORACLE_SID=$(nmap $(echo $IP_ADDRESS) --script oracle-sid-brute | grep oracle-sid-brute -A 1 | grep _ | awk '{print $2}')
fi