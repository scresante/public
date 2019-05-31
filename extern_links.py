#!/usr/bin/env python3
import os
# from sys import argv

def find_external_links(path='.'):
    broke_links, ex_links = [], []
    cur_dev = os.stat(path).st_dev
    for (lpath, dirs, files) in os.walk(path):
        files += dirs
        if files:
            for fname in files:
                fullname = os.path.join(lpath, fname)
                try:
                    stats = os.stat(fullname)
                except FileNotFoundError:
                    broke_links.append(fullname)
                    continue
                if cur_dev != stats.st_dev:
                    ex_links.append(fullname)
    return {'external links': ex_links, 'broken links': broke_links}


if __name__ == "__main__":
    q = find_external_links()
    print(q)
