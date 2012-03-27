#!/usr/bin/env python

#-------------------------------------
# Filename: hrefFinder.py
#-------------------------------------
# Author Email: pete.zhut@gmail.com
#-------------------------------------

import sgmllib

class LocalParser(sgmllib.SGMLParser):
    LINKS = []
    def __init__(self):
        sgmllib.SGMLParser.__init__(self)

    def start_a(self, attrs):
        for name, value in attrs:
            if name.lower() == 'href':
                self.LINKS.append(value)

if __name__ == '__main__':
    import urllib
    p = LocalParser()
    p.feed(urllib.urlopen("http://www.python.org").read())
    print("\n".join(p.LINKS))
