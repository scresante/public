#!/usr/bin/python
import ConfigParser
from os import chdir,listdir
chdir('/etc/NetworkManager/system-connections')
files = listdir('.')
for f in files:
    config = ConfigParser.RawConfigParser()
    config.read(f)
    try:
        config.get('connection','autoconnect')
    except:
        print(f + ' : no autoconnect set  writing false')
        config.set('connection','autoconnect','false')
    print config.items('connection')
    fwriteme = open(f,'w')
    config.write(fwriteme)
    fwriteme.close()

