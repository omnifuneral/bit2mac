# Bitwarden to iCloud Keychain Converter

A Python utility script to convert Bitwarden password exports to a format compatible with Apple's iCloud Keychain. This tool makes it easy to migrate your passwords from Bitwarden to Apple's ecosystem while maintaining data integrity and security.

## Prerequisites

- Python 3.6 or higher
- Bitwarden CLI (for exporting)
- macOS with Safari browser
- Bitwarden account with stored passwords

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/bitwarden-to-icloud.git
cd bitwarden-to-icloud
```

2. Make the script executable:
```bash
chmod +x bw_to_icloud.py
```

3. Install Bitwarden CLI (if not already installed):
```bash
brew install bitwarden-cli
```

## Usage

1. Export your Bitwarden vault:
```bash
bw login
bw export --format json --output ~/Desktop/bitwarden-export.json
```

2. Run the conversion script:
```bash
./bw_to_icloud.py ~/Desktop/bitwarden-export.json ~/Desktop/icloud-import.csv
```

3. Import to iCloud Keychain:
- Open Safari
- Go to File > Import From > CSV file...
- Select the generated `icloud-import.csv` file
- Follow the prompts to complete the import

4. Clean up sensitive files:
```bash
rm -P ~/Desktop/bitwarden-export.json ~/Desktop/icloud-import.csv
```

## Security Considerations

This script handles sensitive password data. Please note:

- Never commit password export files to version control
- Use secure file deletion (`rm -P`) to remove export files
- Keep exported files only on your local machine
- Delete export files immediately after successful import
- Verify your imports before deleting your Bitwarden account
- Don't share export files through insecure channels

## How It Works

The script:
1. Reads the Bitwarden JSON export
2. Extracts login items (usernames, passwords, URLs, etc.)
3. Converts the data to iCloud Keychain's expected CSV format
4. Properly handles special characters and CSV escaping
5. Creates a formatted CSV file ready for Safari import

## Troubleshooting

Common issues and solutions:

- **"File not found" error**: Ensure the path to your export file is correct
- **"Invalid JSON" error**: Make sure your Bitwarden export is complete and not corrupted
- **Empty URLs**: Some entries might have missing URLs - this is normal
- **Special characters**: The script handles these automatically
- **Import fails in Safari**: Ensure the CSV file is properly formatted and not open in another program

If you encounter issues:
1. Check the error message for specific details
2. Verify your Bitwarden export is complete
3. Ensure you have the necessary permissions
4. Try re-exporting from Bitwarden if problems persist

## License

MIT License

Copyright (c) 2023

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

