import random
import os
import urllib
import re
from bs4 import BeautifulSoup

class Twitter(object):
    def _cmd_t(self, cirno, username, args):
                if not args:
                        return
                user_name = args
                tw_user=re.sub('#[^#]+#', '', args)
                try:
                        content=urllib.urlopen("https://mobile.twitter.com/"+tw_user).read()
                except:
                        return
                soup = BeautifulSoup(content,  "lxml")
                tdivs = soup.findAll("div", { "class" : "tweet-text" })
                i=0
                max_t=5
                if len(tdivs) == 0:
                        tdivs = soup.findAll("div", { "class" : "protected" })
                        if len(tdivs) > 0:
                                response=tdivs[i].text.replace('\n',' ').replace('\t','')
                                response=" ".join(response.split())
                                cirno.sendmsg(+user_name+" "+response)
                        else:
                                tdivs = soup.findAll("div", { "class" : "title" })
                                if len(tdivs) > 0:
                                        response=tdivs[i].text.replace('\n',' ').replace('\t','')
                                        response=" ".join(response.split())
                                        cirno.sendmsg("@"+user_name+" "+response)
                        return
                if len(tdivs) < 5:
                        max_t=len(tdivs)
                while i < max_t:
                        tweet=tdivs[i].text.replace('\n',' ').replace('\t','')
                        tweet=" ".join(tweet.split())
                        cirno.sendmsg("@"+user_name+" "+str(i+1)+" "+tweet)
                        i += 1

def setup():
    return Twitter()
