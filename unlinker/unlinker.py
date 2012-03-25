#!/usr/bin/env python

import os
import sys
import shutil

def handleLink(item, action):
    try:
        if os.path.islink(item):
            rp = os.path.realpath(item)
            os.unlink(item)
            print("%s is a link to: %s" % (item, os.path.realpath(item)))
            if action == 'copy':
                if os.path.isdir(item):
                    shutil.copytree(rp, item)
                else:
                    shutil.copy(rp, item)
            elif action == 'move':
                shutil.move(rp, item)
        else:
            return
    except IOError, e:
        print(str(e))

def readDir(**kwargs):
    startingDir = kwargs.get('startingDir', os.getcwd())
    os.chdir(kwargs['dir'])
    print("Current Working Dir: %s" % (os.path.abspath(os.getcwd())))
    for item in os.listdir("."):
        if os.path.isdir(item): 
            readDir(dir=item, startingDir=startingDir)
        handleLink(item, kwargs['action'])
    os.chdir(startingDir)

if __name__ == '__main__':
    try:
        action = sys.argv[1]
        dir = sys.argv[2]
    except:
        if sys.argv[1].strip().lower() not in ['copy', 'move']:
            print("You need an action (copy|move) for this program")
            sys.exit(1)
        else:
            dir = "."
    readDir(action=action.strip().lower(), dir=dir)
