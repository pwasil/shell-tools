#!/usr/bin/python3

import re
import requests

def get_mirrors():
    re_url = re.compile('#Server = (https:\/\/.*)\$repo\/os\/\$arch')
    mirrorlist_url = 'https://www.archlinux.org/mirrorlist'
    payload = {'country': 'all', 'protocol': 'https', 'ip_version': '4', 'use_mirror_status': 'on'}
    mirrorlist_reply = requests.get(mirrorlist_url, params=payload).text
    return re_url.findall(mirrorlist_reply)

def get_archiso(url):
    re_iso = re.compile('<a href="(archlinux-[0-9]{4}\.[0-9]{2}\.[0-9]{2}-x86_64\.iso)">.*<\/a>')
    http_dir = 'iso/latest/'
    http_dir_listing = requests.get(url + http_dir).text
    iso_url = re_iso.findall(http_dir_listing)[0]
    if iso_url is None:
        raise FileNotFoundError()
    file = requests.get("{}{}{}".format(url, http_dir, iso_url))
    with open(iso_url, 'wb') as f:
        f.write(file.content)


if __name__ == "__main__":
    for i in get_mirrors():
        try:
            print('getting image from ', i)
            get_archiso(i)
        except IndexError as e:
            print('link not found')
            continue
        except KeyboardInterrupt as e:
            print('\ninterrupted by keyboard')
            exit(1)
        except FileNotFoundError as e:
            print('file not found')
            continue
        else:
            print('done!')
            break