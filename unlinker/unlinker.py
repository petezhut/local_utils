#!/usr/bin/env python

import os
import sys
import shutil

def moveLink(item):
    try:
        if os.path.islink(item):
            rp = os.path.realpath(item)
            print("%s is a link to: %s" % (item, os.path.realpath(item)))
            os.unlink(item)
            shutil.move(rp, item)
        else:
            return
    except IOError, e:
        print(str(e))

def readDir(**kwargs):
    startingDir = kwargs.get('startingDir', os.getcwd())
    os.chdir(kwargs['dir'])
    print("Current Dir: %s" % (os.path.abspath(os.getcwd())))
    for item in os.listdir("."):
        if os.path.isdir(item): 
            readDir(dir=item, startingDir=startingDir)
        moveLink(item)
    os.chdir(startingDir)

if __name__ == '__main__':
    if len(sys.argv[1:]) <> 1:
        dir = "."
    else:
        dir = sys.argv[-1]
    readDir(dir=dir)
