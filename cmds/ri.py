import urllib
import sys
from bs4 import BeautifulSoup

class Riddle(object):
    def _cmd_rq(self, cirno, username, args):
        e_http="https://riddles.fyi/random-riddles/"
        a = urllib.urlopen(e_http,'').read()
        soup = BeautifulSoup(a)
        tdivs = soup.findAll("a", {"class": "query-title-link"})
        tdivs1 = soup.findAll("div", {"class": "su-spoiler-content su-u-clearfix su-u-trim"})
        for i in tdivs:
            cirno.rq=i.text
            break
        for i in tdivs1:
            cirno.ra=i.text
            break

        cirno.sendmsg("Riddle : "+cirno.rq)

    def _cmd_ra(self, cirno, username, args):
        if cirno.ra != "":
                cirno.sendmsg('%s = %s' % (cirno.rq, cirno.ra))
                cirno.ra= ""
        else:
                cirno.sendmsg('%s: Nothing to answer :doublef' % (username))

def setup():
    return Riddle()
