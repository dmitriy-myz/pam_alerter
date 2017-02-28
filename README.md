place `alerter.py` to `/opt/scripts/`

set up variables on top of alerter.py


add to end of `/etc/pam.d/sshd`
```
session optional pam_exec.so /opt/scripts/alerter.py
```

