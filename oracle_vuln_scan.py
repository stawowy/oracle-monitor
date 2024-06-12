#!/usr/bin/env python3

import os
import subprocess
import sys
import re
import argparse

def parse_nmap_output(nmap_output):
    # Regular expression to match CVEs and their scores
    cve_pattern = re.compile(r'(CVE-\d{4}-\d+)\s+(\d+\.\d+)')
    
    # Find all matches in the Nmap output
    matches = re.findall(cve_pattern, nmap_output)
    
    return matches

def scan(target):
    scan_script = f"""
        #!/bin/bash
        echo 'Vulnerability scan results:\n'
        nmap -sV --script nmap-vulners/ {target} -p 1521
        """

    contents = subprocess.run(
                ['bash', '-c', scan_script],
                check=True, capture_output=True, text=True
            )

    vulns = parse_nmap_output(contents)

    if (len(vulns) > 0):
        subprocess.run(
            [
                'python3', 'mail.py', 
                '--receiver_email', os.environ["DST_MAIL"],
                '--subject', "Nagios vulnerability scan results"
                '--body', contents
            ])
        for cve, score in vulns:
            score = float(score)
            if (score > 7.0):
                print("CRITICAL - Critical vulnerabilities found!")
                sys.exit(2)
        print("WARNING - Vulnerabilities found!")
        sys.exit(1)
    print("OK - No vulnerability found.")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Scan for Oracle DB vulnerabilities.')
    parser.add_argument('--target_addr', type=str, required=True, help='IP address of target server')
    
    args = parser.parse_args()

    scan(args.target_addr)

if __name__ == "__main__":
    main()