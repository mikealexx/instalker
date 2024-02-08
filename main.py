import configparser
import os
from instagrapi import Client
from instagrapi import exceptions

EXPORTS_FOLDER = "exports"


def ensure_exports_folder_exists(username):
    username_folder = os.path.join(EXPORTS_FOLDER, username)
    if not os.path.exists(username_folder):
        os.makedirs(username_folder)


def export_usernames_to_file(usernames, username):
    ensure_exports_folder_exists(username)
    filename = get_next_filename(username)
    filepath = os.path.join(EXPORTS_FOLDER, username, filename)
    with open(filepath, 'w') as file:
        for username in usernames:
            file.write(username + '\n')
    print(f"Usernames exported to {filepath}")
    return filepath


def get_next_filename(username):
    i = 1
    while True:
        filename = f"{i}.txt"
        filepath = os.path.join(EXPORTS_FOLDER, username, filename)
        if not os.path.exists(filepath):
            return filename
        i += 1


def compare_exports(current_file, previous_file):
    new_usernames = set()
    missing_usernames = set()
    if os.path.exists(previous_file):
        with open(previous_file, 'r') as file:
            previous_usernames = set(file.read().splitlines())
        with open(current_file, 'r') as file:
            current_usernames = set(file.read().splitlines())

        new_usernames = current_usernames - previous_usernames
        missing_usernames = previous_usernames - current_usernames

    return new_usernames, missing_usernames


def main():
    if not os.path.exists('creds.ini'):
        print("Run setup.py first to provide Instagram credentials.")
        return

    config = configparser.ConfigParser()
    config.read('creds.ini')
    username = config['instagram'].get('username', '')
    password = config['instagram'].get('password', '')

    if not (username and password):
        print("Invalid creds.ini file. Please run setup.py again.")
        return

    cl = Client()
    try:
        cl.login(username, password)
    except exceptions.PleaseWaitFewMinutes:
        print("Please wait a few minutes before trying again")
        return

    user_id = cl.user_id_from_username(username)
    following = cl.user_following(user_id=user_id)
    usernames = [f.username for f in following.values()]

    current_file = export_usernames_to_file(usernames, username)

    if current_file == os.path.join(EXPORTS_FOLDER, username, "1.txt"):
        print("First export")
    else:
        previous_number = int(current_file.split('/')[-1].split('.')[0]) - 1
        previous_file = os.path.join(EXPORTS_FOLDER, username, f"{previous_number}.txt")
        new_usernames, missing_usernames = compare_exports(current_file, previous_file)
        if not (new_usernames or missing_usernames):
            print("There was no change in the following list.")
        if new_usernames:
            print(f"{username} followed these accounts:")
            for new_username in new_usernames:
                print(new_username)
        if missing_usernames:
            print(f"{username} unfollowed these accounts:")
            for missing_username in missing_usernames:
                print(missing_username)


if __name__ == "__main__":
    main()
