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


def is_connected():
    test_host = 'www.google.com'
    port = 80
    timeout = 2
    try:
        print('Checking your connection to the Internet...')
        s = socket.create_connection((test_host, port), timeout)
        print('Connected.\n')
        s.close()
    except Exception:
        print("No connection. Attention!!! Script will work without verification remote blacklists.\n" )
        return False
    return True


def is_local_blacklist(filepath):
    if filepath:
        return True
    else:
        print('Local blacklist has not been declared by user. Script will works without verification local blacklist.\n')
        return False


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


def is_password_in_blacklists(password, *blacklists_stack):
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
                    '"password minimum length (8 characters)"': '[A-Za-z\d]{8,}',
                    '"special characters"': '\W+'
                    }

    if blacklist_inspection and password not in personal_data.values():
        print('Passed test of: "into blacklists and personal data"')
        for name, pattern in strength_criteria.items():
            response_status = re.search(pattern, password)
            if response_status:
                print('Passed test of: {}'.format(name))
                strength_password += 2
            else:
                print('Not passed test of: {}'.format(name))
        return strength_password
    else:
        print('Your password has been found in some of blacklists or your personal data:')
        return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Password Strength Calculator')
    parser.add_argument('-l', '--local', help="path to local blacklist or filename for current directory.")
    args = parser.parse_args()

    local_blacklist = get_local_blacklist(args.local) if is_local_blacklist(args.local) else None
    remote_blacklist = get_remote_blacklist(REMOTE_BLACKLISTS) if is_connected() else None

    personal_data = collect_presonal_data()
    usr_password = getpass(prompt='Type your password: ')
    print('Calculating strength of your password, please wait...')

    password_rating = get_password_strength(usr_password, personal_data, is_password_in_blacklists(usr_password, local_blacklist, remote_blacklist))
    print('Strength of your password: {} of 10\n'.format(password_rating))
