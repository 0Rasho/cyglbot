import random
import os

class Ddice(object):
    def _cmd_dd(self, cirno, username, args):
        cirno.sendmsg("%s => %d %d\n\0" %
               (username, random.randint(1,6), random.randint(1,6)))

def setup():
    return Ddice()
