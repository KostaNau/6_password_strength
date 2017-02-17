import argparse
from getpass import getpass
from itertools import chain
import socket
import re

import requests



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
        s = socket.create_connection((test_host, port), timeout)
        s.close()
    except socket.gaierror:
        return False
    return True


def collect_presonal_data():
    personal_data = {
        '1. Given Name': None,
        '2. Family Name': None,
        '3. City of Birth': None,
        '4. Date of Brith':None,
        '5. Your Phone Number': None,
        }

    for question in sorted(personal_data):
        user_answer = input('{}: '.format(question))
        personal_data[question] = user_answer
    return personal_data


def get_blacklists(remote_links, local_path=False):
    if local_path:
        with open(local_path, 'r') as blacklist_file:
            local_blacklist = blacklist_file.read().rsplit()
            yield from local_blacklist
    if is_connected():
        for list_link in remote_links.values():
            remote_blacklist = requests.get(list_link).text.rsplit()
            yield from remote_blacklist


def get_password_strength(password, personal_data, blacklist_inspection):
    strength_password = {}
    strength_criteria = {
                    '"digit"': '(?=.*?\d)',
                    '"uppercase"': '(?=.*?[A-Z])',
                    '"lowercase"': '(?=.*?[a-z])',
                    '"password minimum length (8 characters)"': '[A-Za-z\d]{8,}',
                    '"special characters"': '\W+'
                    }

    if not blacklist_inspection and password not in personal_data.values():
        for name, pattern in strength_criteria.items():
            response_status = re.search(pattern, password)
            if response_status:
                strength_password[name] = 2
        return strength_password
    else:
        return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Password Strength Calculator')
    parser.add_argument('-l', '--local',
                        default=None,
                        help="path to local blacklist or filename for current directory.")
    args = parser.parse_args()

    usr_password = getpass(prompt='Type your password: ')
    personal_data = collect_presonal_data()
    blacklists = get_blacklists(REMOTE_BLACKLISTS, args.local)
    print('Please wait...')
    blacklist_inspection_result = any(usr_password in x for x in blacklists)
    password_rating = get_password_strength(usr_password, personal_data, blacklist_inspection_result)
    if password_rating == 0:
        print('Your password has been found in some of blacklists or your personal data. Please try again!')
    else:
        print('Strength of your password: {} of 10'.format(sum(password_rating.values())))
        for test in password_rating.keys():
            print('Passed test of {}'.format(test))
