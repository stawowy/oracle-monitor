FROM jasonrivers/nagios

RUN apt-get update &&\
    apt-get install -y nmap alien libaio1 rpm dos2unix &&\
    #install vulners plugin
    cd /usr/share/nmap/scripts/ &&\
    git clone https://github.com/vulnersCom/nmap-vulners.git &&\
    # install Oracle CLI for check_oracle_health
    cd / &&\
    wget https://download.oracle.com/otn_software/linux/instantclient/2340000/oracle-instantclient-basic-23.4.0.24.05-1.el8.x86_64.rpm &&\
    wget https://download.oracle.com/otn_software/linux/instantclient/2340000/oracle-instantclient-devel-23.4.0.24.05-1.el8.x86_64.rpm &&\
    wget https://download.oracle.com/otn_software/linux/instantclient/2340000/oracle-instantclient-sqlplus-23.4.0.24.05-1.el8.x86_64.rpm &&\
    alien -i oracle-instantclient-basic-23.4.0.24.05-1.el8.x86_64.rpm &&\
    alien -i oracle-instantclient-devel-23.4.0.24.05-1.el8.x86_64.rpm &&\
    alien -i oracle-instantclient-sqlplus-23.4.0.24.05-1.el8.x86_64.rpm &&\
    # echo 'export ORACLE_HOME=/usr/lib/oracle/23/client64/' >> /etc/profile &&\
    # echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME/lib' >> /etc/profile &&\
    # echo 'export PATH=${ORACLE_HOME}bin:$PATH' >> /etc/profile &&\
    export ORACLE_HOME=/usr/lib/oracle/23/client64/ &&\
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME/lib &&\
    export PATH=${ORACLE_HOME}bin:$PATH &&\
    # exec $SHELL &&\
    rm /oracle-instant* &&\
    # install check_oracle_health
    echo 'yes' | perl -MCPAN -e 'install DBI' &&\
    echo 'yes' | perl -MCPAN -e 'install DBD::Oracle' &&\
    cd /root/.cpan/build/$(ls /root/.cpan/build | grep DBD) &&\
    perl Makefile.PL &&\
    make &&\
    make install &&\
    mkdir /software &&\
    cd /software/ &&\
    wget https://labs.consol.de/assets/downloads/nagios/check_oracle_health-3.3.2.1.tar.gz &&\
    tar xzf check_oracle_health-3.3.2.1.tar.gz &&\
    rm *.tar.gz &&\
    cd check_oracle_health-3.3.2.1 &&\
    ./configure -prefix=/usr/local/nagios -with-nagios-user=nagios &&\
    make &&\
    make install &&\
    # get required scripts
    cd /home &&\
    mkdir reports &&\
    git clone https://github.com/stawowy/oracle-monitor.git &&\
    cd oracle-monitor &&\
    dos2unix ip_finder.sh &&\
    dos2unix scan.sh &&\
    dos2unix start_nagios &&\
    chmod +x ip_finder.sh &&\
    chmod +x scan.sh &&\
    rm /usr/local/bin/start_nagios &&\
    mv start_nagios /usr/local/bin &&\
    chmod +x /usr/local/bin/start_nagios

CMD ["/usr/local/bin/start_nagios"] 