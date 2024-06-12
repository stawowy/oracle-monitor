#!/usr/bin/env python3

# Init file for the Nagios configuration

import subprocess
import os
import sys
import textwrap

oracle_modes = ["connection-time", "connected-users", "session-usage", 
                "process-usage", "tablespace-usage"]

def add_plugin_path():
    print("Adding path to plugins...")
    try:
        with open("/opt/nagios/etc/resource.cfg", 'a') as resource:
            resource.write(textwrap.dedent(
                """
                # Store path to custom plugins
                $USER5$=/usr/local/nagios/libexec 
                """))
    except FileNotFoundError:
        print("File not found.")

def set_contact():
    print("Setting admin e-mail...")

    dest_addr = os.environ["DST_MAIL"]
    with open("/opt/nagios/etc/objects/contacts.cfg", 'w') as contacts:
        contacts.write(textwrap.dedent(
            f"""
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
        ))

def add_host():
    try:
        with open("/home/oracle-monitor/IP_ADDRESS.txt", 'r') as ipaddr:
            ip_address = ipaddr.readline().strip()
    except FileNotFoundError:
        print("Failed to get IP address of database server.")
        ip_address = input("Provide IP address of database server: ")
    
    try:
        with open("/opt/nagios/etc/objects/host.cfg", 'w') as host:
            host.write(textwrap.dedent(
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
                """))
    except FileExistsError:
        print("Host already configured.")


def add_commands():
    try:
        with open("/home/oracle-monitor/ORACLE_SID.txt", 'r') as orasid:
            sid = orasid.readline().strip()
    except FileNotFoundError:
        print("Failed to get SID.")

    print("Adding nagios commands...")
    dbuname = os.environ["DB_USER"]
    dbpass = os.environ["DB_PASS"]
    try:
        # Write the updated content back to commands.cfg
        with open("/opt/nagios/etc/objects/commands.cfg", 'w') as commands:
            commands.write(textwrap.dedent(
                """
                # 'notify-host-by-email' command definition
                define command{
                    command_name    notify-host-by-email
                    command_line    /usr/bin/printf "\%b" "***** Nagios *****\\n\\nNotification Type: $NOTIFICATIONTYPE$\\nHost: $HOSTNAME$\\nState: $HOSTSTATE$\\nAddress: $HOSTADDRESS$\\nInfo: $HOSTOUTPUT$\\n\\nDate/Time: $LONGDATETIME$\\n" | /usr/bin/mail -s "** $NOTIFICATIONTYPE$ Host Alert: $HOSTNAME$ is $HOSTSTATE$ **" $CONTACTEMAIL$
                }

                # 'notify-service-by-email' command definition
                define command {
                    command_name        notify-service-by-email
                    command_line        $USER5$/send_email.py --receiver_email $CONTACTEMAIL$ --subject "Service Alert: $SERVICEDESC$ on $HOSTNAME$ is $SERVICESTATE$" --body "Service $SERVICEDESC$ on host $HOSTNAME$ is $SERVICESTATE$. \\nAdditional Info: \\n$SERVICEOUTPUT$"
                }


                # This command checks to see if a host is "alive" by pinging it
                # The check must result in a 100% packet loss or 5 second (5000ms) round trip 
                # average time to produce a critical error.
                # Note: Five ICMP echo packets are sent (determined by the '-p 5' argument)

                # 'check-host-alive' command definition
                define command{
                    command_name    check-host-alive
                    command_line    $USER1$/check_ping -H $HOSTADDRESS$ -w 3000.0,80\% \-c 5000.0,100% -p 5
                }


                # 'check_local_disk' command definition
                define command{
                    command_name    check_local_disk
                    command_line    $USER1$/check_disk -w $ARG1$ -c $ARG2$ -p $ARG3$
                }


                # 'check_local_load' command definition
                define command{
                    command_name    check_local_load
                    command_line    $USER1$/check_load -w $ARG1$ -c $ARG2$
                }


                # 'check_local_procs' command definition
                define command{
                    command_name    check_local_procs
                    command_line    $USER1$/check_procs -w $ARG1$ -c $ARG2$ -s $ARG3$
                }


                # 'check_local_users' command definition
                define command{
                    command_name    check_local_users
                    command_line    $USER1$/check_users -w $ARG1$ -c $ARG2$
                }   


                # 'check_local_swap' command definition
                define command{
                    command_name    check_local_swap
                    command_line    $USER1$/check_swap -w $ARG1$ -c $ARG2$
                }


                # 'check_local_mrtgtraf' command definition
                define command{
                    command_name    check_local_mrtgtraf
                    command_line    $USER1$/check_mrtgtraf -F $ARG1$ -a $ARG2$ -w $ARG3$ -c $ARG4$ -e $ARG5$
                }


                # 'check_ftp' command definition
                define command{
                    command_name    check_ftp
                    command_line    $USER1$/check_ftp -H $HOSTADDRESS$ $ARG1$
                }


                # 'check_hpjd' command definition
                define command{
                    command_name    check_hpjd
                    command_line    $USER1$/check_hpjd -H $HOSTADDRESS$ $ARG1$
                }


                # 'check_snmp' command definition
                define command{
                    command_name    check_snmp
                    command_line    $USER1$/check_snmp -H $HOSTADDRESS$ $ARG1$
                }


                # 'check_http' command definition
                define command{
                    command_name    check_http
                    command_line    $USER1$/check_http -I $HOSTADDRESS$ $ARG1$
                }


                # 'check_ssh' command definition
                define command{
                    command_name    check_ssh
                    command_line    $USER1$/check_ssh $ARG1$ $HOSTADDRESS$
                }


                # 'check_dhcp' command definition
                define command{
                    command_name    check_dhcp
                    command_line    $USER1$/check_dhcp $ARG1$
                }


                # 'check_ping' command definition
                define command{
                    command_name    check_ping
                    command_line    $USER1$/check_ping -H $HOSTADDRESS$ -w $ARG1$ -c $ARG2$ -p 5
                }


                # 'check_pop' command definition
                define command{
                    command_name    check_pop
                    command_line    $USER1$/check_pop -H $HOSTADDRESS$ $ARG1$
                }


                # 'check_imap' command definition
                define command{
                    command_name    check_imap
                    command_line    $USER1$/check_imap -H $HOSTADDRESS$ $ARG1$
                }


                # 'check_smtp' command definition
                define command{
                    command_name    check_smtp
                    command_line    $USER1$/check_smtp -H $HOSTADDRESS$ $ARG1$
                }


                # 'check_tcp' command definition
                define command{
                        command_name    check_tcp
                        command_line    $USER1$/check_tcp -H $HOSTADDRESS$ -p $ARG1$ $ARG2$
                    }


                # 'check_udp' command definition
                define command{
                    command_name    check_udp
                    command_line    $USER1$/check_udp -H $HOSTADDRESS$ -p $ARG1$ $ARG2$
                }


                # 'check_nt' command definition
                define command{
                    command_name    check_nt
                    command_line    $USER1$/check_nt -H $HOSTADDRESS$ -p 12489 -v $ARG1$ $ARG2$
                }


                define command {
                    command_name    process-service-perfdata
                    command_line    /opt/nagiosgraph/bin/insert.pl
                }
                """
            ))


        with open("/opt/nagios/etc/objects/commands.cfg", 'a') as commands:
            commands.write(textwrap.dedent(
                f"""
                define command {{
                    command_name        check_oracle_health_tnsping
                    command_line        $USER5$/check_oracle_health --connect=$HOSTADDRESS$:1521/{sid} --mode tnsping
                }}
                
                define command {{
                    command_name        oracle_scan_vulnerabilities
                    command_line        python3 $USER5$/oracle_vuln_scan.py --target_addr $HOSTADDRESS$
                }}\n
                """))

            for mode in oracle_modes:
                command = textwrap.dedent(f"""
                define command {{
                    command_name        check_oracle_health_{mode}
                    command_line        $USER5$/check_oracle_health --connect=$HOSTADDRESS$:1521/{sid} --username={dbuname} --password={dbpass} --mode {mode}
                }}\n
                """)
                commands.write(command)
    except FileNotFoundError:
        print("File not found.")

def add_services():
    print("Adding nagios services...")
    try:
        with open("/opt/nagios/etc/objects/services.cfg", 'w') as services:
            service = textwrap.dedent("""
            define service {
                use                     generic-service
                host_name               oracle
                service_description     Tnsping
                check_command           check_oracle_health_tnsping
                notification_options    c,w
                contacts                nagiosadmin
                check_interval          5
            }

            define service {
                use                     generic-service
                host_name               oracle
                service_description     Scan oracle DB for vulnerabilities
                check_command           oracle_scan_vulnerabilities
                notification_options    c,w
                contacts                nagiosadmin
                check_interval          5
            }
            """)
            services.write(service)

            for mode in oracle_modes:
                service = textwrap.dedent(f"""
                define service {{
                    use                     generic-service
                    host_name               oracle
                    service_description     {mode.replace('-', ' ').title()}
                    check_command           check_oracle_health_{mode}
                    notification_options    c,w
                    contacts                nagiosadmin
                    check_interval          5
                }}\n
                """)
                services.write(service)
    except FileNotFoundError:
        print("File not found.")

def configure():
    print("Final config...")
    try:
        with open("/opt/nagios/etc/nagios.cfg", 'a') as nagios:
            nagios.write(textwrap.dedent(
                """
                # Custom config for Oracle DB
                cfg_file=/opt/nagios/etc/objects/host.cfg
                cfg_file=/opt/nagios/etc/objects/services.cfg
                """))
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