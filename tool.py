#!/usr/bin/env python3
"""
Phone Number Information Lookup Tool
An advanced utility to retrieve phone number information based on country codes
Version: 2.0
"""

import re
import json
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import argparse
import sys
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for terminal colors
init(autoreset=True)


class PhoneNumberInfo:
    """Main class for phone number information lookup"""

    def __init__(self):
        self.country_codes = self._load_country_codes()

    def _load_country_codes(self):
        """Load country code database"""
        return {
            '+62': {'country': 'Indonesia', 'emoji': '🇮🇩'},
            '+1': {'country': 'USA / Canada', 'emoji': '🇺🇸'},
            '+44': {'country': 'United Kingdom', 'emoji': '🇬🇧'},
            '+61': {'country': 'Australia', 'emoji': '🇦🇺'},
            '+60': {'country': 'Malaysia', 'emoji': '🇲🇾'},
            '+65': {'country': 'Singapore', 'emoji': '🇸🇬'},
            '+63': {'country': 'Philippines', 'emoji': '🇵🇭'},
            '+66': {'country': 'Thailand', 'emoji': '🇹🇭'},
            '+84': {'country': 'Vietnam', 'emoji': '🇻🇳'},
            '+81': {'country': 'Japan', 'emoji': '🇯🇵'},
            '+82': {'country': 'South Korea', 'emoji': '🇰🇷'},
            '+86': {'country': 'China', 'emoji': '🇨🇳'},
            '+91': {'country': 'India', 'emoji': '🇮🇳'},
            '+92': {'country': 'Pakistan', 'emoji': '🇵🇰'},
            '+93': {'country': 'Afghanistan', 'emoji': '🇦🇫'},
            '+94': {'country': 'Sri Lanka', 'emoji': '🇱🇰'},
            '+95': {'country': 'Myanmar', 'emoji': '🇲🇲'},
            '+98': {'country': 'Iran', 'emoji': '🇮🇷'},
            '+7': {'country': 'Russia / Kazakhstan', 'emoji': '🇷🇺'},
            '+33': {'country': 'France', 'emoji': '🇫🇷'},
            '+49': {'country': 'Germany', 'emoji': '🇩🇪'},
            '+39': {'country': 'Italy', 'emoji': '🇮🇹'},
            '+34': {'country': 'Spain', 'emoji': '🇪🇸'},
            '+55': {'country': 'Brazil', 'emoji': '🇧🇷'},
            '+27': {'country': 'South Africa', 'emoji': '🇿🇦'},
            '+20': {'country': 'Egypt', 'emoji': '🇪🇬'},
            '+234': {'country': 'Nigeria', 'emoji': '🇳🇬'},
            '+254': {'country': 'Kenya', 'emoji': '🇰🇪'},
        }

    def validate_phone_number(self, phone_number):
        """Validate and normalize phone number format"""
        phone_number = re.sub(r'\s+', '', phone_number)
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        return phone_number

    def get_country_info(self, phone_number):
        """Get country information from phone number prefix"""
        for code in sorted(self.country_codes.keys(), key=len, reverse=True):
            if phone_number.startswith(code):
                return self.country_codes[code], code
        return None, None

    def parse_with_phonenumbers(self, phone_number):
        """Parse phone number using phonenumbers library"""
        try:
            parsed = phonenumbers.parse(phone_number)

            info = {
                'valid': phonenumbers.is_valid_number(parsed),
                'possible': phonenumbers.is_possible_number(parsed),
                'national_number': parsed.national_number,
                'country_code': parsed.country_code,
                'region': geocoder.description_for_number(parsed, "en"),
                'carrier': carrier.name_for_number(parsed, "en"),
                'timezones': timezone.time_zones_for_number(parsed),
                'number_type': phonenumbers.number_type(parsed)
            }

            type_map = {
                0: "FIXED_LINE",
                1: "MOBILE",
                2: "FIXED_LINE_OR_MOBILE",
                3: "TOLL_FREE",
                4: "PREMIUM_RATE",
                5: "SHARED_COST",
                6: "VOIP",
                7: "PERSONAL_NUMBER",
                8: "PAGER",
                9: "UAN",
                10: "VOICEMAIL",
                27: "UNKNOWN"
            }

            info['number_type_str'] = type_map.get(info['number_type'], "UNKNOWN")
            return info

        except Exception as e:
            return {'error': str(e)}

    def lookup_external_api(self, phone_number):
        """Optional lookup using external APIs"""
        apis = [
            {
                'name': 'numverify',
                'url': 'http://apilayer.net/api/validate',
                'params': {
                    'access_key': 'YOUR_API_KEY',
                    'number': phone_number,
                    'format': 1
                }
            }
        ]

        results = []
        for api in apis:
            try:
                response = requests.get(api['url'], params=api['params'], timeout=10)
                if response.status_code == 200:
                    results.append({
                        'api': api['name'],
                        'data': response.json()
                    })
            except Exception:
                continue

        return results

    def format_phone_number(self, phone_number, country_code=None):
        """Format phone number for better readability"""
        if country_code:
            national = phone_number.replace(country_code, '')

            if country_code == '+62':
                if len(national) == 10:
                    return f"{national[:4]}-{national[4:7]}-{national[7:]}"
                elif len(national) == 11:
                    return f"{national[:4]}-{national[4:8]}-{national[8:]}"
            elif country_code == '+1' and len(national) == 10:
                return f"({national[:3]}) {national[3:6]}-{national[6:]}"
        return phone_number

    def display_info(self, phone_number, country_info, country_code, parsed_info):
        """Display phone number information"""
        print(f"\n{Fore.CYAN}{'=' * 60}")
        print(f"{Fore.YELLOW}📱 PHONE NUMBER INFORMATION LOOKUP")
        print(f"{Fore.CYAN}{'=' * 60}")

        print(f"\n{Fore.GREEN}📞 Phone Number: {Fore.WHITE}{phone_number}")

        if country_info:
            print(f"{Fore.GREEN}🌍 Country: {Fore.WHITE}{country_info['emoji']} {country_info['country']}")
            print(f"{Fore.GREEN}🔢 Country Code: {Fore.WHITE}{country_code}")

        formatted = self.format_phone_number(phone_number, country_code)
        if formatted != phone_number:
            print(f"{Fore.GREEN}📋 Formatted: {Fore.WHITE}{formatted}")

        print(f"\n{Fore.CYAN}{'─' * 40}")
        print(f"{Fore.YELLOW}🔍 DETAILS")
        print(f"{Fore.CYAN}{'─' * 40}")

        if 'error' in parsed_info:
            print(f"{Fore.RED}❌ Error: {parsed_info['error']}")
            return

        print(f"{Fore.GREEN}✓ Valid: {parsed_info['valid']}")
        print(f"{Fore.GREEN}✓ Possible: {parsed_info['possible']}")
        print(f"{Fore.GREEN}✓ National Number: {parsed_info['national_number']}")
        print(f"{Fore.GREEN}✓ Region: {parsed_info.get('region', 'N/A')}")
        print(f"{Fore.GREEN}✓ Carrier: {parsed_info.get('carrier', 'N/A')}")
        print(f"{Fore.GREEN}✓ Time Zones: {', '.join(parsed_info.get('timezones', []))}")
        print(f"{Fore.GREEN}✓ Number Type: {parsed_info.get('number_type_str', 'UNKNOWN')}")

        print(f"\n{Fore.YELLOW}⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.CYAN}{'=' * 60}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Phone Number Information Lookup Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:
  tool.py +6281234567890
  tool.py 081234567890
  tool.py --file numbers.txt
        """
    )

    parser.add_argument('phone_number', nargs='?', help='Phone number to lookup')
    parser.add_argument('-f', '--file', help='File containing phone numbers')
    parser.add_argument('-o', '--output', help='Save output to JSON file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-l', '--list-countries', action='store_true', help='List supported country codes')

    args = parser.parse_args()
    tool = PhoneNumberInfo()

    if args.list_countries:
        for code, info in tool.country_codes.items():
            print(f"{code} - {info['country']} {info['emoji']}")
        return

    if not args.phone_number and not args.file:
        print("Please provide a phone number or use --file.")
        return

    results = []

    if args.phone_number:
        number = tool.validate_phone_number(args.phone_number)
        info, code = tool.get_country_info(number)
        parsed = tool.parse_with_phonenumbers(number)
        tool.display_info(number, info, code, parsed)

        results.append({
            'phone_number': number,
            'country': info['country'] if info else None,
            'parsed_info': parsed,
            'timestamp': datetime.now().isoformat()
        })

    if args.output and results:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
