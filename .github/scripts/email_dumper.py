#!/usr/bin/env python3

import argparse, re

from datetime import datetime
from os import mkdir
from os.path import dirname, exists, realpath

from redbox import EmailBox as redbox


parser = argparse.ArgumentParser(description='Dump a IMAP folder into .eml files')
parser.add_argument('-s',
                    dest='host',
                    help='IMAP host',
                    default='imap.gmail.com')
parser.add_argument('-P',
                    dest='port',
                    help='IMAP port',
                    default=993)
parser.add_argument('-u',
                    dest='username',
                    help='IMAP username',
                    required=True)
parser.add_argument('-p',
                    dest='password',
                    help='IMAP password',
                    required=True)
parser.add_argument('-r',
                    dest='remote',
                    help='Remote folder to download',
                    default='INBOX')
parser.add_argument('-l',
                    dest='local',
                    help='Local folder where to save .eml files',
                    default=f'emails')
parser.add_argument('-U',
                    dest='unread',
                    help='Keep emails unread in the inbox',
                    default=False,
                    action=argparse.BooleanOptionalAction)

args = parser.parse_args()

mail = redbox(host=args.host,
              port=args.port,
              username=args.username,
              password=args.password)

messages = mail[args.remote].search(unseen=True)
date_now = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

print(f'[{date_now}] New {len(messages)} requests!')

if not exists(args.local):
    mkdir(args.local)


for message in messages:
    try:
        index = messages.index(message) + 1
        output = f'{args.local}/{index}.eml'
        date = message.date.strftime('%Y-%m-%d %H:%M:%S')
        compinfo = re.search('(.*)\nhttp', message.text_body).group(1).strip()
        print(f'[{date}] [{index}] {compinfo}')
        with open(output, 'w', newline='') as file:
            file.write(message.content)
    except:
        continue
    finally:
        if args.unread:
            message.unread()