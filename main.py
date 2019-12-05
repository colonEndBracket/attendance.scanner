#!/usr/bin/env python3
import smtplib
from datetime import datetime
from email.message import EmailMessage

import pandas as pd

from credentials import password, username


def send_email(guests, event_name):
    with open("notify_list.txt","r") as ntfy:
        notify_list = ntfy.readlines()
        now = datetime.now().date()
        people = ""
        for person in guests:
            people += (person+"\n")
        msg = EmailMessage()
        msg['Subject'] = f'[{now}] {len(guests)} guests attended {event_name}'
        msg.set_content(
f"""
People who attended {event_name}:
~~~~~~~~~~~~~~~~~~~~~~~
{people}
"""
        )

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(username, notify_list, str(msg))
        server.quit()

        ntfy.close()

def main():
    names = pd.read_csv("card_data.csv", delimiter=', ', engine='python')
    guest_list = []
    for (first, last) in zip(names['First Name'], names['Last Name']):
        guest_list.append(str(first+" "+last))
    #for row in names:
    #    print(row[0]+row[1])
    send_email(guest_list,"It's Alive!")
    
if __name__ == "__main__":
    main()
