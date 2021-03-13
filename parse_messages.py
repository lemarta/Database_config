import argparse
from models import Message, User
from psycopg2 import connect
from clcrypto import check_password

cnx = connect(host='localhost', user='postgres', password='coderslab', database='db_workshop')
cnx.autocommit = True
cursor = cnx.cursor()

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-t", "--to", help="message recipient")
parser.add_argument("-s", "--send", help="message text (max 255 characters)")
parser.add_argument("-l", "--list", help="list all messages", action="store_true")

args = parser.parse_args()

if args.list and args.username and args.password and not args.send and not args.to:
    user_list_by_username = User.load_user_by_username(cursor=cursor, username=args.username)
    if user_list_by_username:
        if check_password(pass_to_check=args.password, hashed=user_list_by_username.hashed_password):
            messages = Message.load_all_messages(cursor=cursor)
            for message in messages:
                user_data_by_id = User.load_user_by_id(cursor=cursor, id_=message.from_id)
                if message.to_id == user_list_by_username.id:
                    print('From', user_data_by_id.username, ':', message.text, '- Sent on', message.creation_date)
        else:
            print('Incorrect password')
    else:
        print('User not found')
elif args.username and args.password and args.send and args.to and not args.list:
    user_find_by_username = User.load_user_by_username(cursor=cursor, username=args.username)
    if user_find_by_username:
        if check_password(pass_to_check=args.password, hashed=user_find_by_username.hashed_password):
            recipient_find_by_username = User.load_user_by_username(cursor=cursor, username=args.to)
            if recipient_find_by_username:
                if len(args.send) <= 255:
                    message = Message(user_find_by_username.id, recipient_find_by_username.id, args.send)
                    message.save_to_db(cursor=cursor)
                else:
                    excess = len(args.send) - 255
                    print(f'Message too long by {excess} characters. Please shorten your message and try again.')
            else:
                print('Recipient not found')
        else:
            print('Incorrect password')
    else:
        print('User not found')
else:
    parser.print_help()
