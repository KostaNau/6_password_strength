import argparse
from getpass import getpass
import requests
import socket
import re


REMOTE_BLACKLISTS = {
                'link': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/10_million_password_list_top_1000000.txt',
                'gmail password': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/alleged-gmail-passwords.txt',
                'webhost password': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/000webhost.txt',
                'keyboard combination': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/KeyboardCombinations.txt',
                'md5decryptor': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/md5decryptor.uk.txt'
                }


def check_connection():
    test_host = 'www.google.com'
    port = 80
    timeout = 2
    try:
        print('Checking your connection to the Internet...')
        s = socket.create_connection((test_host, port), timeout)
        print('Connected.')
        s.close()
    except Exception:
        print("No connection.\n" )
        return False
    return True


def collect_presonal_data():
    personal_data = {
        'Given Name': None,
        'Family Name': None,
        'Date of Brith':None,
        'Your Phone Number': None,
        'City of Brith': None
        }

    for question in sorted(personal_data):
        user_answer = input('{}: '.format(question))
        personal_data[question] = user_answer
    return personal_data


def get_remote_blacklist(remote_links):
    for list_link in remote_links.values():
        remote_blacklist = requests.get(list_link).text.rsplit()
        yield remote_blacklist


def get_local_blacklist(local_path):
    with open(local_path, 'r') as blacklist_file:
        local_blacklist = blacklist_file.read().rsplit()
        return local_blacklist


def check_blacklists(password, blacklists_stack):
    for black_lists in blacklists_stack:
        if black_lists == None:
            continue
        for black_list in black_lists:
            if password in black_list:
                return False
    return True


def get_password_strength(password, personal_data, blacklist_inspection):
    strength_password = 0
    strength_criteria = {
                    '"digit"': '(?=.*?\d)',
                    '"uppercase"': '(?=.*?[A-Z])',
                    '"lowercase"': '(?=.*?[a-z])',
                    '"password minimum length"': '[A-Za-z\d]{8,}',
                    '"Special characters"': '\W_'
                    }

    if blacklist_inspection and password not in personal_data.values():
        for name, pattern in strength_criteria.items():
            response_status = re.search(pattern, password)
            if response_status:
                print('Passed test of: {}'.format(name))
                strength_password += 2
            else:
                print('Not passed test of: {}'.format(name))
        return strength_password
    else:
        return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Password Strength Calculator')
    parser.add_argument('-l', '--local', help="path to local blacklist or filename for current directory.")
    args = parser.parse_args()

    local_blacklist = get_local_blacklist(args.local) if args.local else None
    remote_blacklist = get_remote_blacklist(REMOTE_BLACKLISTS) if check_connection() else None
    all_blacklists = (local_blacklist, remote_blacklist)
    if not any(all_blacklists):
        print("WARNING!!! \nInternet connection has not been established...\nLocal blacklist has not been found...\nPassword checking in the blacklist is not available!\n")

    personal_data = collect_presonal_data()
    usr_password = getpass(prompt='Type your password: ')
    print('Calculating strength of your password, please wait...')

    password_rating = get_password_strength(usr_password, personal_data, check_blacklists(usr_password, all_blacklists))
    print('Strength of your password: {} of 10'.format(password_rating))
