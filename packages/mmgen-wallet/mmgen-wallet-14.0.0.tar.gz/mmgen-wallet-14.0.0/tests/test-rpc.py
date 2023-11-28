#!/usr/bin/env python3

import sys,os,time
from pprint import pprint
from mmgen.util import *
from mmgen.common import *

cmd_args = opts.init({'text': { 'desc': '', 'usage':'', 'options':'' }})

rpc_init()
pmsg(g.rpch.daemon_version >= 190100)
# 190600
