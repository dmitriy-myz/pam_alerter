#!/usr/bin/python

import os
import json
import sys
store_dir = "/var/lib/pam_alerter"


user = os.getenv('PAM_USER')
host = os.getenv('PAM_RHOST', 'unknown')
service = os.getenv('PAM_SERVICE', 'unknown')
pam_type = os.getenv('PAM_TYPE')
pam_tty = os.getenv('PAM_TTY')


if not os.path.isdir(store_dir):
    os.makedirs(store_dir)


def load_settings(filename):
    try:
        with open(filename, 'r') as f:
            ips = json.load(f)
    except:
        ips = []
    return ips

def save_settings(filename, settings):
    with open(filename, 'w') as f:
        json.dump(settings, f, indent=4, sort_keys=True)

if user != os.path.basename(user):
    print "strange user: '%s'!" % user
    sys.exit();

ip_list_per_user = os.path.join(store_dir, user)

known_ips = load_settings(ip_list_per_user)


if pam_type != 'close_session':
    if host not in known_ips:
        print "Login by: %s from: %s\n\nservice = %s pam_type = %s" % (user, host, service, pam_type)
        known_ips.append(host)
        save_settings(ip_list_per_user, known_ips)
    #printf "%b" "Hello, \n\nLogin by ${PAM_USER} from ${PAM_RHOST}\n\n $(printenv)" | mail -s "Login alert" dmitriy.myz@livetex.ru
