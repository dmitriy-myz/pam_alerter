#!/usr/bin/python
import os
import json
import sys
import smtplib
from email.mime.text import MIMEText


store_dir = '/var/lib/pam_alerter'
settings_file = 'alerter.json'


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
            settings = json.load(f)
    except:
        settings = []
    return settings

def save_settings(filename, settings):
    with open(filename, 'w') as f:
        json.dump(settings, f, indent=4, sort_keys=True)

def send_email(message):
    msg = MIMEText(message, 'plain')
    msg['Subject'] = 'Login alert for %s' % user
    msg['From']   = sender
    msg['To'] = receivers[0]
    smtpObj = smtplib.SMTP('localhost')
    smtpObj.sendmail(sender, receivers, msg.as_string())


script_directory = os.path.dirname(os.path.abspath(__file__))
mail_settings_file = os.path.join(script_directory, settings_file)

mail_settings = load_settings(mail_settings_file)
sender = mail_settings['sender']
receivers = mail_settings['receivers']


# security check
if user != os.path.basename(user):
    message =  'strange user: "%s"!' % user
    send_email(message)
    sys.exit();

ip_list_per_user = os.path.join(store_dir, user)

known_ips = load_settings(ip_list_per_user)


if pam_type != 'close_session':
    if host not in known_ips:
        message = 'Login by: %s from: %s\n\nservice = %s pam_type = %s' % (user, host, service, pam_type)
        send_email(message)
        known_ips.append(host)
        save_settings(ip_list_per_user, known_ips)

