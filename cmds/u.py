import random
import os
import urllib
import re
from bs4 import BeautifulSoup
from lib.urban import urban_define

class Urban(object):
    def _cmd_u(self, cirno, username, args):
                if not args:
                        return
                define=urban_define(str(args))
                if define == None:
                        cirno.sendmsg(":cray"+ " Sorry " + args + " not found :sadbye")
                else:
                        cirno.sendmsg(args + " : " + define)

def setup():
    return Urban()
