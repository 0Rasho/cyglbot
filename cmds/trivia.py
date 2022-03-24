import random
import os
import urllib
from html.parser import HTMLParser
import re
import requests
from bs4 import BeautifulSoup
from random import randrange
from threading import Timer
athread=None
def timer_thr( cirno, username):
      if cirno.trivia_answer != "":
            cirno.sendmsg1('%s: Trivia Ans => %s' % (username, cirno.trivia_answer))
            cirno.trivia_answer=""
            cirno.trivia_opt=""
'''
"9">General Knowledge
"10">Entertainment: Books
"11">Entertainment: Film
"12">Entertainment: Music
"13">Entertainment: Musicals &amp; Theatres
"14">Entertainment: Television
"15">Entertainment: Video Games
"16">Entertainment: Board Games
"17">Science &amp; Nature
"18">Science: Computers
"19">Science: Mathematics
"20">Mythology
"21">Sports
"22">Geography
"23">History
"24">Politics
"25">Art
"26">Celebrities
"27">Animals
"28">Vehicles
"29">Entertainment: Comics
"30">Science: Gadgets
"31">Entertainment: Japanese Anime &amp; Manga
"32">Entertainment: Cartoon &amp; Animations

"09">General Knowledge
"10">Entertainment: Books
"11">Entertainment: Film
"12">Entertainment: Music
"14">Entertainment: Television
"17">Science &amp; Nature
"18">Science: Computers
"19">Science: Mathematics
"21">Sports
"22">Geography
"23">History
"24">Politics
"25">Art
"26">Celebrities
"30">Science: Gadgets
'''

cat=[9,10,11,12,14,17,18,19,21,22,23,24,25,26,30]


class Trivia(object):
    def _cmd_t(self, cirno, username, args):
                i=0
                ct=random.choice(cat)
                r = requests.get("https://opentdb.com/api.php?amount=1&category="+str(ct))
                q = r.json()['results'][0]
                qtype = q['type']
                h = HTMLParser()
                question = h.unescape(q['question'])
                cirno.trivia_answer = q['correct_answer']
                ians = q['incorrect_answers']
                ians.insert(randrange(len(ians)+1),cirno.trivia_answer)
                i = 1
                options = ""
                for opt in ians:
                        options += str(i) +") "+ opt + " "
                        i = i + 1
                        
                cirno.trivia_opt=options
                if qtype == 'boolean':
                        cirno.sendmsg('Trivia ? => %s (True/False)' % (question))
                else:
                        cirno.sendmsg('Trivia ? => %s ' % (question))
                        cirno.sendmsg('Options => %s' % (cirno.trivia_opt))
                timeout=30
                if args:
                    try:
                        timeout=int(args)
                    except:
                        timeout=30
                try:
                    athread.cancel()
                except:
                    pass
                athread = Timer(timeout, timer_thr, [cirno, username])
                athread.start()

    def _cmd_a(self, cirno, username, args):
                if cirno.trivia_answer != "":
                        cirno.sendmsg('%s: Trivia Ans => %s' % (username, cirno.trivia_answer))
                        cirno.trivia_answer=""
                        cirno.trivia_opt=""
                else:
                        cirno.sendmsg('%s: Nothing to answer :doublef' % (username))
    def _cmd_o(self, cirno, username, args):
                if cirno.trivia_opt != "":
                        cirno.sendmsg('%s: Trivia Options => %s' % (username, cirno.trivia_opt))
                else:
                        cirno.sendmsg('%s: Nothing to answer :doublef' % (username))

#    def _cmd_t(self, cirno, username, args):
#               try:
#                       content=urllib.urlopen("http://trivia.fyi/").read()
#                       content=urllib.urlopen("http://trivia.fyi/random-questions?page=1").read()
#               except:
#                       pass
#               soup = BeautifulSoup(content, "html.parser")
#               qdivs = soup.findAll("h2", { "class" : "title" })
#               adivs = soup.findAll("div", { "class" : "spoiler-content" })
#               if len(adivs) > 0 and len(qdivs) > 0:
#                       question = qdivs[0].text
#                       answer = adivs[0].text
#                       cirno.trivia_answer=answer
#                       cirno.sendmsg('%s: Trivia ? => %s' % (username, question))
#
#   def _cmd_a(self, cirno, username, args):
#               if cirno.trivia_answer != "":
#                       cirno.sendmsg('%s: Trivia Ans => %s' % (username, cirno.trivia_answer))
#                       cirno.trivia_answer=""
#               else:
#                       cirno.sendmsg('%s: Nothing to answer :doublef' % (username))
def setup():
    return Trivia()
