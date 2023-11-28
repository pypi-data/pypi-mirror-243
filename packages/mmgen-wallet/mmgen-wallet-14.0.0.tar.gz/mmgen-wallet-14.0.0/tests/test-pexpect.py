#!/usr/bin/env python3

import sys,os,ast
#from pexpect.popen_spawn import PopenSpawn as spawn
from pexpect import spawn

# from mmgen.common import *
# from mmgen.obj import *
# cmd_args = opts.init(lambda: { 'desc': '', 'usage':'', 'options':'' })

p = spawn('./spawnprog.py foo bar',encoding='utf8')
ret = p.expect('hello: ')
print('got: {}'.format(ret))
print('before: [{}]'.format(p.before))
print('after: [{}]'.format(p.after))
print('groups: {}'.format(p.match.groups()))
ret = p.send('x')
ret = p.read()
print('got: ' + ret)
