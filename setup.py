import configparser

def save_credentials(username, password):
    config = configparser.ConfigParser()
    config['instagram'] = {'username': username, 'password': password}

    with open('creds.ini', 'w') as configfile:
        config.write(configfile)

    print("Login credentials saved successfully.")

def main():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")

    save_credentials(username, password)

    # # Update main.py with new credentials
    # with open('main.py', 'r') as file:
    #     lines = file.readlines()
    #
    # for i, line in enumerate(lines):
    #     if 'cl.login(' in line:
    #         lines[i] = f'    cl.login("{username}", "{password}")\n'
    #
    # with open('main.py', 'w') as file:
    #     file.writelines(lines)
    #
    # print("main.py updated with new credentials.")

if __name__ == "__main__":
    main()
