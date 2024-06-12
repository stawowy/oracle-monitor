#!/usr/bin/env python3

# Init file for the Nagios configuration

import subprocess
import os
import sys

oracle_modes = ["connection-time", "connected-users", "session-usage", 
                "process-usage", "tablespace-usage"]

def add_plugin_path():
    print("Adding path to plugins...")
    try:
        with open("/opt/nagios/etc/resource.cfg", 'a') as resource:
            resource.write(
                """
                # Store path to custom plugins
                $USER5$=/usr/local/nagios/libexec 
                """)
    except FileNotFoundError:
        print("File not found.")

def set_contact():
    print("Setting admin e-mail...")

    dest_addr = os.environ["DST_MAIL"]
    with open("/opt/nagios/etc/objects/contacts.cfg", 'w') as contacts:
        contacts.write(
            f"""
            ###############################################################################
            # CONTACTS.CFG - SAMPLE CONTACT/CONTACTGROUP DEFINITIONS
            #
            #
            # NOTES: This config file provides you with some example contact and contact
            #        group definitions that you can reference in host and service
            #        definitions.
            #
            #        You don't need to keep these definitions in a separate file from your
            #        other object definitions.  This has been done just to make things
            #        easier to understand.
            #
            ###############################################################################



            ###############################################################################
            #
            # CONTACTS
            #
            ###############################################################################

            # Just one contact defined by default - the Nagios admin (that's you)
            # This contact definition inherits a lot of default values from the
            # 'generic-contact' template which is defined elsewhere.

            define contact {{

                contact_name                    nagiosadmin             ; Short name of user
                use                             generic-contact         ; Inherit default values from generic-contact template (defined above)
                alias                           Nagios Admin            ; Full name of user
                service_notification_options    w,c                     ; send notifications on WARNING and CRITICAL states
                service_notification_commands   notify-service-by-email ;
                email                           {dest_addr}
            }}



            ###############################################################################
            #
            # CONTACT GROUPS
            #
            ###############################################################################

            # We only have one contact in this simple configuration file, so there is
            # no need to create more than one contact group.

            define contactgroup {{

                contactgroup_name       admins
                alias                   Nagios Administrators
                members                 nagiosadmin
            }}
            """
        )

def add_host():
    try:
        with open("/home/oracle-monitor/IP_ADDRESS.txt", 'r') as ipaddr:
            ip_address = ipaddr.readline()
    except FileNotFoundError:
        print("Failed to get IP address of database server.")
        ip_address = input("Provide IP address of database server: ")
    
    try:
        with open("/opt/nagios/etc/objects/host.cfg", 'w') as host:
            host.write(
                f"""
                define host {{
                    use                     linux-server
                    host_name               oracle
                    alias                   Oracle Database Server
                    address                 {ip_address}
                    check_period            24x7
                    max_check_attempts      5
                    notification_period     24x7
                    }}
                """)
    except FileExistsError:
        print("Host already configured.")


def add_commands():
    try:
        with open("/home/oracle-monitor/ORACLE_SID.txt", 'r') as orasid:
            sid = orasid.readline()
    except FileNotFoundError:
        print("Failed to get SID.")

    print("Adding nagios commands...")
    dbuname = os.environ["DB_USER"]
    dbpass = os.environ["DB_PASS"]
    try:
        with open("/opt/nagios/etc/objects/commands.cfg", 'r') as file:
            # Replace old definition of notify-service-by-email
            new_mail_notif = """
            define command {
                command_name        notify-service-by-email
                command_line        $USER5$/send_email.py --receiver_email $CONTACTEMAIL$ --subject "Service Alert: $SERVICEDESC$ on $HOSTNAME$ is $SERVICESTATE$" --body "Service $SERVICEDESC$ on host $HOSTNAME$ is $SERVICESTATE$. \n\nAdditional Info:\n\n$SERVICEOUTPUT$"
            }
            """ 
            lines = file.readlines()

            # Find and delete the old command definition (notify-service-by-email)
            start_index = None
            end_index = None
            for i, line in enumerate(lines):
                if 'command_name    notify-service-by-email' in line:
                    start_index = i
                elif start_index is not None and line.strip().startswith('}'):
                    end_index = i
                    break

            # Delete the old command definition if found
            if start_index is not None and end_index is not None:
                del lines[start_index:end_index + 1]

            # Insert the new command definition at the end of the file
            lines.append(new_mail_notif + '\n')

        # Write the updated content back to commands.cfg
        with open("/opt/nagios/etc/objects/commands.cfg", 'w') as file:
            file.writelines(lines)


        with open("/opt/nagios/etc/objects/commands.cfg", 'a') as commands:
            commands.write(
                f"""
                define command {{
                    command_name        check_oracle_health_tnsping
                    command_line        $USER5$/check_oracle_health --connect=$HOSTADDRESS$:1521/{sid} --mode tnsping
                }}
                
                define command {{
                    command_name        oracle_scan_vulnerabilities
                    command_line        $USER5$/oracle_vuln_scan.py --target_addr $HOSTADDRESS$
                }}\n
                """)

            for mode in oracle_modes:
                command = f"""
                define command {{
                    command_name        check_oracle_health_{mode}
                    command_line        $USER5$/check_oracle_health --connect=$HOSTADDRESS$:1521/{sid} --username={dbuname} --password={dbpass} --mode {mode}
                }}\n
                """
                commands.write(command)
    except FileNotFoundError:
        print("File not found.")

def add_services():
    print("Adding nagios services...")
    try:
        with open("/opt/nagios/etc/objects/services.cfg", 'w') as services:
            service = """
            define service {
                use                     generic-service
                host_name               oracle
                service_description     Scan oracle DB for vulnerabilities
                check_command           oracle_scan_vulnerabilities
                notification_options    c,w
                contacts                admin
                check_interval          5
            }
            """
            services.write(service)

            for mode in oracle_modes:
                service = f"""
                define service {{
                    use                     generic-service
                    host_name               oracle
                    service_description     {mode.replace('-', ' ').title()}
                    check_command           check_oracle_health_{mode}
                    notification_options    c,w
                    contacts                admin
                    check_interval          5
                }}\n
                """
                services.write(service)
    except FileNotFoundError:
        print("File not found.")

def configure():
    print("Final config...")
    try:
        with open("/opt/nagios/etc/nagios.cfg", 'a') as nagios:
            nagios.write(
                """
                # Custom config for Oracle DB
                cfg_file=/opt/nagios/etc/objects/host.cfg
                cfg_file=/opt/nagios/etc/objects/services.cfg
                """)
    except FileNotFoundError:
        print("File not found.")

if __name__ == "__main__":
    print("Initializing target, might take a while.")
    subprocess.call(['sh', '/home/oracle-monitor/ip_finder.sh'])
    print("Done.")
    print("Configuring Nagios services for Oracle DB...")

    add_plugin_path()
    set_contact()
    add_host()
    add_commands()
    add_services()
    configure()

    print("Done. Check localhost:8080")
    sys.exit(0)