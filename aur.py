#!/bin/python3

import requests
import subprocess
from datetime import datetime as dt
import argparse

api_url = 'https://aur.archlinux.org/rpc'
aur_url = 'https://aur.archlinux.org'

def aur_query(payload: dict) -> dict:
    return requests.get(api_url, params=payload).json()


def aur_info(query_arg: str) -> dict:
    return aur_query({'v': '5', 'type': 'info', 'arg': query_arg})


def aur_search(query_arg: str, query_searchby='name') -> dict:
    return aur_query({'v': '5', 'type': 'search', 'by': query_searchby, 'arg': query_arg})


if __name__ == "__main__":
    def aur_prettyprint(data):
        class ShellColors:
            head = '\033[95m'
            blue = '\033[94m'
            green = '\033[92m'
            warn = '\033[93m'
            fail = '\033[91m'
            reset = '\033[0m'
            bold = '\033[1m'
            under = '\033[4m'

        time_format = '%Y-%m-%d %H:%M:%S'
        print('    {} | {}'.format(
            ShellColors.head + data['type'],
            str(data['resultcount'] if data['type'] != 'error' else data['error']) + ShellColors.reset))

        for i in data['results']:
            print('{} | {} | {} | {} | {} | {}\n    {}'.format(
                ShellColors.warn + ShellColors.bold + i['Name'] + ShellColors.reset,
                ShellColors.green + i['Version'] + ShellColors.reset,
                ShellColors.green + str(i['Maintainer']) + ShellColors.reset,
                ShellColors.green + str(i['Popularity']) + ShellColors.blue + ShellColors.reset,
                ShellColors.blue + dt.fromtimestamp(i['FirstSubmitted']).strftime(time_format) + ShellColors.reset,
                ShellColors.blue + dt.fromtimestamp(i['LastModified']).strftime(time_format) + ShellColors.reset,
                i['Description']))


    def aur_install(data):
        for i in data['results']:
            print('installing', i['Name'])
            subprocess.run(['/bin/bash', 'aur-install.sh', '--name', i['Name'], '--url', aur_url + i['URLPath']])


    action_map = {'search': lambda query: aur_prettyprint(aur_search(query)),
                  'info': lambda query: aur_prettyprint(aur_info(query)),
                  'install': lambda query: print('not implemented yet')}

    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs='?', metavar='action', choices=action_map.keys())
    parser.add_argument('package', nargs='?', metavar='package')
    args = vars(parser.parse_args())

    action_map[args['action']](args['package'])
