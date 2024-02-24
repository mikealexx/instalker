# Instalker: Instagram OSINT Tool

Instalker is an open-source OSINT (Open Source Intelligence) project designed to analyze Instagram accounts by exporting followers and following users, and then comparing the current and previous exports to identify new or lost followers/following users. The tool serves as a utility for individuals or organizations interested in monitoring changes in their Instagram audience.

## Features

- **Export Followers/Following**: Instalker allows users to export the list of followers and following users from a specified Instagram account.
- **Comparison Analysis**: After at least one export, Instalker compares the current and last export to identify new followers/following users or those who have been lost.
- **Simple Interface**: The tool provides a straightforward command-line interface for easy interaction.

## Installation

1. Clone the Instalker repository to your local machine:
   ```bash
   git clone https://github.com/mikealexx/instalker.git
2. Navigate to the project directory:
   ```bash
   cd instalker
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

1. Enter your Instagram account credentials by running:
   ```bash
   python3 setup.py
   ```
   Only necessary at first run or when changing the credentials.

2. Run the Instalker script:
   ```bash
   python3 instalker.py <instagram_username>
   ```

   Replace `<instagram_username>` with the username of the Instagram account you wish to analyze.

## Example

```bash
git clone https://github.com/mikealexx/instalker.git
cd instalker
python3 setup.py
python3 instalker.py _mikealexx
```

## Security and Credentials

Instalker requires Instagram API credentials for accessing Instagram data. These credentials are stored locally in the `creds.ini` file within the project directory. It's important to note that Instalker does not share or use these credentials publicly.

### Protection of Credentials

The security of your credentials is of utmost importance. Instalker ensures that your credentials are securely stored locally and are not exposed to the public. However, it's recommended to take additional precautions to protect your credentials, such as restricting access to the `creds.ini` file and avoiding sharing it with unauthorized individuals.

### Responsible Usage

It's essential to use Instalker responsibly and in compliance with Instagram's terms of service. Avoid sharing your credentials or using Instalker for unauthorized or unethical purposes. By using Instalker, you agree to take full responsibility for the security and appropriate usage of your credentials.

## Disclamer

Instalker is intended for educational and research purposes only. The developers do not endorse any unauthorized or unethical use of this tool. Users are responsible for complying with Instagram's terms of service and respecting the privacy of others.

## Contributions

Contributions to Instalker are welcome! If you have suggestions for improvements, bug fixes, or new features, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [License](LICENSE) file for details.
