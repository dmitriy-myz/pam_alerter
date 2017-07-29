# pam alerter

Script for alert to email if user logged in from new ip address

## Prerequisites
working local mta, listening on localhost

## install
place `alerter.py` to `/opt/scripts/`

place `alerter.json` to `/opt/scripts/` 

set sender email, receivers, ip white list in `alerter.json` 

add to the end of file `/etc/pam.d/sshd`
```
session optional pam_exec.so /opt/scripts/alerter.py
```
voila!
