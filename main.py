import configparser
import os
import sys
import shutil
from instagrapi import Client, exceptions

EXPORTS_FOLDER = "exports"
CREDS_FILE = 'creds.ini'


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


def clean_user_exports(username):
    user_folder = os.path.join(EXPORTS_FOLDER, username)
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)
        print(f"Exports for user '{username}' cleaned successfully.")
    else:
        print(f"No exports found for user '{username}'.")


def clean_all_exports():
    if os.path.exists(EXPORTS_FOLDER):
        shutil.rmtree(EXPORTS_FOLDER)
        print("All exports cleaned successfully.")
    else:
        print("No exports found.")


def clean_credentials():
    if os.path.exists(CREDS_FILE):
        os.remove(CREDS_FILE)
        print("Credentials cleaned successfully.")
    else:
        print("No credentials found.")


def main(username):
    if not os.path.exists(CREDS_FILE):
        print("Run setup.py first to provide Instagram credentials.")
        return

    config = configparser.ConfigParser()
    config.read(CREDS_FILE)
    username_saved = config['instagram'].get('username', '')
    password = config['instagram'].get('password', '')

    if not (username_saved and password):
        print("Invalid creds.ini file. Please run setup.py again.")
        return

    cl = Client()
    try:
        cl.login(username_saved, password)
    except exceptions.PleaseWaitFewMinutes:
        print("Please wait a few minutes before trying again")
        return

    user_id = cl.user_id_from_username(username)

    for export_type in ["followers", "following"]:
        usernames = get_usernames(cl, user_id, export_type)
        export_usernames_to_file(usernames, username, export_type)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("""Usage: python3 main.py <flag>
Flags:
    -u <username>: Analyze followers/following usernames of the specified <username>.
    -cu <username>: Clean the information gathered about the specified <username>.
    -cA: Clean all usernames' exports.
    -cC: Clean credentials.""")
    elif args[0] == '-u' and len(args) == 2:
        main(args[1])
    elif args[0] == '-cu' and len(args) == 2:
        clean_user_exports(args[1])
    elif args[0] == '-cA' and len(args) == 1:
        clean_all_exports()
    elif args[0] == '-cC' and len(args) == 1:
        clean_credentials()
    else:
        print("Invalid flag or usage. See usage instructions.")
        sys.exit(1)
