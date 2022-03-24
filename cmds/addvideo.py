from time import sleep
from bs4 import BeautifulSoup
from lib.utils import parsemedialink, filterchat


class Addvideo(object):

    def _cmd_add(self, cirno, username, data):
        if data:
            pos = 'next'
            temp = True
            duration = 0
            data = filterchat(data)
            x = parsemedialink(data)
            cirno.addvideo(0, None, None, duration, temp, pos, x)


def setup():
    return Addvideo()
