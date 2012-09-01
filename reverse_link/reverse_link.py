#!/usr/bin/env python

import os
import sys
import shutil

def reverse_links(data):
    # data is a tuple of linked path, origin path
    current_link, actual_link = data
    # 1. Remove the old link
    os.unlink(current_link)
    # 2. Move data from origin to link dir (preserving the name)
    if os.path.isdir(actual_link):
        shutil.copytree(actual_link, current_link)
        shutil.rmtree(actual_link)
    else:
        shutil.copy(actual_link, current_link)
        os.remove(actual_link)
    # 3. Link back to the origin form the link dir
    os.symlink(current_link, actual_link)

if __name__ == '__main__':
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    links = filter(lambda x: os.path.islink(os.path.join(directory, x)), os.listdir(directory))
    for count, link in enumerate(links, 1):
        print("Working on #%d of %d" % (count, len(links)))
        reverse_links((os.path.abspath(os.path.join(directory, link)), os.path.realpath(os.path.join(directory, link))))
