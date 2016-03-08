#!/usr/bin/env python

from subprocess import call, Popen, PIPE

cmd = 'sudo cp test.sh /usr/bin'
call(cmd, shell=True)
cmd = 'sudo chmod 755 /usr/bin/test.sh'
call(cmd, shell=True)
cmd = 'sudo test.sh'
call(cmd, shell=True)
