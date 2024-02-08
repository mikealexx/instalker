import configparser
import os
import sys
from instagrapi import Client
from instagrapi import exceptions

EXPORTS_FOLDER = "exports"


def ensure_exports_folder_exists(username):
    username_folder = os.path.join(EXPORTS_FOLDER, username)
    for export_type in ["followers", "following"]:
        export_type_folder = os.path.join(username_folder, export_type)
        if not os.path.exists(export_type_folder):
            os.makedirs(export_type_folder)


def export_usernames_to_file(usernames, username, export_type):
    ensure_exports_folder_exists(username)
    filename = get_next_filename(username, export_type)
    filepath = os.path.join(EXPORTS_FOLDER, username, export_type, filename)
    with open(filepath, 'w') as file:
        for username in usernames:
            file.write(username + '\n')
    print(f"{len(usernames)} usernames exported to {filepath}\n")
    return filepath


def get_next_filename(username, export_type):
    i = 1
    while True:
        filename = f"{i}.txt"
        filepath = os.path.join(EXPORTS_FOLDER, username, export_type, filename)
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


def get_usernames(client, user_id, export_type):
    if export_type == "following":
        data = client.user_following(user_id=user_id)
    elif export_type == "followers":
        data = client.user_followers(user_id=user_id)
    else:
        raise ValueError("Invalid export type")

    return [f.username for f in data.values()]


def main(user_to_track):
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

    user_id = cl.user_id_from_username(user_to_track)

    for export_type in ["followers", "following"]:
        usernames = get_usernames(cl, user_id, export_type)
        current_file = export_usernames_to_file(usernames, user_to_track, export_type)

        if current_file == os.path.join(EXPORTS_FOLDER, user_to_track, export_type, "1.txt"):
            print(f"First export of {export_type}: {len(usernames)+1} usernames exported")
        else:
            previous_number = int(current_file.split('/')[-1].split('.')[0]) - 1
            previous_file = os.path.join(EXPORTS_FOLDER, user_to_track, export_type, f"{previous_number}.txt")
            new_usernames, missing_usernames = compare_exports(current_file, previous_file)
            if not (new_usernames or missing_usernames):
                print(f"There was no change in the {export_type} list.")
            if new_usernames:
                if export_type == "followers":
                    print(f"{user_to_track} gained these {export_type}:")
                    for new_username in new_usernames:
                        print(new_username)
                else:
                    print(f"{user_to_track} is now {export_type}:")
                    for new_username in new_usernames:
                        print(new_username)
            print("")
            if missing_usernames:
                if export_type == "followers":
                    print(f"{user_to_track} lost these {export_type}:")
                    for missing_username in missing_usernames:
                        print(missing_username)
                else:
                    print(f"{user_to_track} stopped {export_type}:")
                    for missing_username in missing_usernames:
                        print(missing_username)
        print("")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <username>")
        sys.exit(1)
    main(sys.argv[1])
