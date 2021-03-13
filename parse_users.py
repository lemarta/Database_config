import argparse
from models import User
from psycopg2 import connect
from clcrypto import check_password

cnx = connect(host='localhost', user='postgres', password='coderslab', database='db_workshop')
cnx.autocommit = True
cursor = cnx.cursor()

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete selected user", action="store_true")
parser.add_argument("-e", "--edit", help="edit selected user", action="store_true")

args = parser.parse_args()

if args.username and args.password and not args.edit and not args.delete and not args.list and not args.new_pass:
    user_list_by_username = User.load_user_by_username(cursor=cursor, username=args.username)
    if user_list_by_username:
        print('User already exists')
    else:
        if len(args.password) >= 8:
            user = User(args.username, args.password)
            user.save_to_db(cursor=cursor)
        else:
            print('Password too short - minimal length is 8 characters')
elif args.new_pass and args.username and args.password and args.edit and not args.delete and not args.list:
    user_list_by_username = User.load_user_by_username(cursor=cursor, username=args.username)
    if user_list_by_username:
        if check_password(pass_to_check=args.password, hashed=user_list_by_username.hashed_password):
            if len(args.new_pass) >= 8:
                user_list_by_username.hashed_password = args.new_pass
                user_list_by_username.save_to_db(cursor=cursor)
            else:
                print('Password too short - minimal length is 8 characters')
        else:
            print('Incorrect password')
    else:
        print('User not found')
elif args.list and not args.username and not args.password and not args.edit and not args.new_pass and not args.delete:
    users = User.load_all_users(cursor=cursor)
    for user in users:
        print('User:', user.id, 'Username:', user.username)
elif args.delete and args.username and args.password and not args.new_pass and not args.list and not args.edit:
    user_list_by_username = User.load_user_by_username(cursor=cursor, username=args.username)
    if user_list_by_username:
        if check_password(pass_to_check=args.password, hashed=user_list_by_username.hashed_password):
            user_list_by_username.delete(cursor=cursor)
        else:
            print('Incorrect password')
    else:
        print('User not found')
else:
    parser.print_help()
