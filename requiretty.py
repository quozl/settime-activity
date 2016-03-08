#!/usr/bin/env python

fin = open('/etc/sudoers','r')
txt = fin.read()
fin.close()
lines = txt.split('\n')
fout = open('/etc/sudoers','w')
for line in lines:
    if 'requiretty' in line:
        if '#' in line:
            line = line.replace('#','')
            print 'requiretty active'
        else:
            line = '#' + line
            print 'tty not required'
    print >> fout, line
fout.close()
