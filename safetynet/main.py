#!/usr/bin/env python

import ConfigReader
import os.path
import datetime
import shutil
import hashlib
import glob

CFG = 'safetynet.cfg'
config = ConfigReader.ConfigReader()
config.read(CFG)

def md5(filepath):
    # Attribution: 
    # http://www.joelverhagen.com/blog/2011/02/md5-hash-of-file-in-python/
    f = open(filepath, 'rb')
    md5 = hashlib.md5()
    while True:
        data = f.read(4096)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

for directory in config.DEFAULT.local_backup_dirs.split(","):
    for filename in filter(lambda x: os.path.join(directory, x) not in glob.glob(os.path.join(directory, config.DEFAULT.ignore)), os.listdir(directory)):
        now = datetime.datetime.now() 
        nowdate = str(now.date())
        nowtime = str(now.time())

        backuppath = os.path.join(config.DEFAULT.remote_backup_dir, nowdate.replace("-", "_"))
        backupfilename = "%s_%s" % (nowtime, filename)

        if not os.path.isdir(backuppath):
            os.mkdir(backuppath)
            if os.path.islink(os.path.join(config.DEFAULT.remote_backup_dir, 'current')): 
                print("Updating the 'current' directory link")
                os.remove(os.path.join(config.DEFAULT.remote_backup_dir, 'current'))
            os.symlink(backuppath, os.path.join(config.DEFAULT.remote_backup_dir, 'current'))
        flag = False
        try:
            backupfiles = os.listdir(backuppath)
            backupfiles.sort()
            if md5(os.path.join(directory, filename)) != md5(os.path.join(backuppath, max(glob.glob(os.path.join(backuppath, "*%s" % (filename))), key = lambda x: os.stat(x).st_mtime))):
                shutil.copy(os.path.join(directory, filename), os.path.join(backuppath, backupfilename))
                print("[%s] - Found a difference, making a copy" % (filename))
                flag = True
        except:
            shutil.copy(os.path.join(directory, filename), os.path.join(backuppath, backupfilename))
            print("[%s] - Didn't find file, copying" % (filename))
            flag = True
        finally:
            if flag:
                if os.path.islink(os.path.join(backuppath, filename)): os.remove(os.path.join(backuppath, filename))
                os.symlink(os.path.join(backuppath, backupfilename), os.path.join(backuppath, filename))
