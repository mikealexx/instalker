import sys
from instagrapi import Client
import os


def ensure_exports_folder_exists(username):
    exports_folder = username
    if not os.path.exists(exports_folder):
        os.makedirs(exports_folder)


def export_usernames_to_file(usernames, username):
    ensure_exports_folder_exists(username)
    filename = get_next_filename(username)
    filepath = os.path.join(username, filename)
    with open(filepath, 'w') as file:
        for username in usernames:
            file.write(username + '\n')
    print(f"Usernames exported to {filepath}")
    return filepath


def get_next_filename(username):
    i = 1
    while True:
        filename = f"{i}.txt"
        filepath = os.path.join(username, filename)
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


def main(username):
    cl = Client()
    cl.login("_mikealexx", "4#RN#UJOWknnG79G&wQom")

    user_id = cl.user_id_from_username(username)
    following = cl.user_following(user_id=user_id, amount=5)
    usernames = [f.username for f in following.values()]

    current_file = export_usernames_to_file(usernames, username)

    if current_file == os.path.join(username, "1.txt"):
        print("First export")
    else:
        previous_number = int(current_file.split('/')[-1].split('.')[0]) - 1
        previous_file = os.path.join(username, f"{previous_number}.txt")
        new_usernames, missing_usernames = compare_exports(current_file, previous_file)
        if new_usernames:
            print(f"{username} followed these accounts:")
            for new_username in new_usernames:
                print(new_username)
        if missing_usernames:
            print(f"{username} unfollowed these accounts:")
            for missing_username in missing_usernames:
                print(missing_username)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <username>")
        sys.exit(1)
    main(sys.argv[1])
