place `alerter.py` to `/opt/scripts/`
place `alerter.json` to `/opt/scripts/`


add to end of `/etc/pam.d/sshd`
```
session optional pam_exec.so /opt/scripts/alerter.py
```

