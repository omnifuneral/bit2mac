#!/usr/bin/env python3

import json
import csv
import sys
import argparse
from pathlib import Path
from typing import Dict, List

def parse_bitwarden_export(json_file: Path) -> List[Dict]:
    """
    Parse Bitwarden JSON export and extract login items.
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Extract only login items
        items = data.get('items', [])
        login_items = [item for item in items if item.get('type') == 1]  # type 1 = login
        return login_items
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON file format - {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to read input file - {e}", file=sys.stderr)
        sys.exit(1)

def convert_to_keychain_format(items: List[Dict]) -> List[Dict]:
    """
    Convert Bitwarden items to iCloud Keychain format.
    """
    keychain_items = []
    
    for item in items:
        try:
            login = item.get('login', {})
            uris = login.get('uris', [])
            url = ''
            if uris and isinstance(uris, list) and len(uris) > 0:
                first_uri = uris[0]
                if isinstance(first_uri, dict):
                    url = first_uri.get('uri', '')
            
            keychain_item = {
                'Title': item.get('name', ''),
                'URL': url,
                'Username': login.get('username', ''),
                'Password': login.get('password', ''),
                'Notes': item.get('notes', ''),
                'OTPAuth': login.get('totp', '')
            }
            keychain_items.append(keychain_item)
        except Exception as e:
            print(f"Warning: Error processing item '{item.get('name', 'Unknown')}': {e}", file=sys.stderr)
            continue
        
    return keychain_items

def write_csv(items: List[Dict], output_file: Path) -> None:
    """
    Write items to CSV file in iCloud Keychain format.
    """
    fieldnames = ['Title', 'URL', 'Username', 'Password', 'Notes', 'OTPAuth']
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(items)
    except Exception as e:
        print(f"Error: Failed to write output file - {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Convert Bitwarden JSON export to iCloud Keychain CSV format',
        epilog='WARNING: Output file will contain sensitive data. Handle with care and delete after import.'
    )
    parser.add_argument('input_file', type=Path, help='Bitwarden JSON export file')
    parser.add_argument('output_file', type=Path, help='Output CSV file for iCloud Keychain')
    args = parser.parse_args()

    # Convert the file
    print("Reading Bitwarden export file...")
    items = parse_bitwarden_export(args.input_file)
    
    print(f"Converting {len(items)} login items...")
    keychain_items = convert_to_keychain_format(items)
    
    print("Writing CSV file...")
    write_csv(keychain_items, args.output_file)
    
    print("\nConversion complete!")
    print("\nIMPORTANT:")
    print("1. Import the CSV file into Safari (File > Import From > CSV file...)")
    print("2. After importing, securely delete both the JSON and CSV files:")
    print(f"   rm -P {args.input_file} {args.output_file}")

if __name__ == '__main__':
    main()

