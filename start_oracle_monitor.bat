echo off

for /f "tokens=3" %%a in ('netsh interface ipv4 show address ^| findstr 192.168.*/24') do echo SUBNET_ADDR=%%a > vars.env

echo.
echo.Input following credentials:
echo.
set /p userdb=DB username for nagios:
set /p passdb=DB password for nagios:
echo.It is recommended that you use g-mail with app passwords to send alerts!
set /p srcemail=Gmail for sending alerts:
set /p srcpass=App password:
set /p dstmail=E-mail to receive alerts:
(echo DB_USER=%userdb%) >> vars.env
(echo DB_PASS=%passdb%) >> vars.env
(echo SRC_MAIL=%srcemail%) >> vars.env
(echo SRC_PASS=%srcpass%) >> vars.env
(echo DST_MAIL=%dstmail%) >> vars.env

echo on

docker run --env-file=vars.env --name oracle-monitor -p 0.0.0.0:8080:80 nagios-oracle-monitor