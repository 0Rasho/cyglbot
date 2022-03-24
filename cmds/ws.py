import random
import os
from PyDictionary import PyDictionary
import requests
from bs4 import BeautifulSoup

words_list=[]
dictionary=PyDictionary()
file1 = open('db/words.txt', 'r')
file1.seek(0, os.SEEK_SET)
for quote in file1:
            quote=quote.strip('\n')
            quote=quote.strip()
            if len(quote) > 5:
                words_list.append(quote.lower())
file1.close()
random.shuffle(words_list)
random.shuffle(words_list)

class Word_Scramble(object):
    def _cmd_sw(self, cirno, username, args):
        if len(words_list) == 0:
                self.update_words()
        try:
                r_fact= words_list.pop()
                #url="http://wordunscrambler.me/random-word-generator"
                #r = requests.get(url)
                #s=BeautifulSoup(r.text)
                #div = s.find(id="random-word-wrapper")
                #r_fact=div.text.strip()
                cirno.wordscramble_answer=r_fact
                cirno.wslen=len(r_fact)
                cirno.clue=0
                shuffle=list(r_fact)
                random.shuffle(shuffle)
                shuffle = ''.join(shuffle)
                cirno.wordscramble=shuffle
                cirno.sendmsg("Scrambled word = "+shuffle)
                cirno.meaning=dictionary.meaning(cirno.wordscramble_answer)
        except:
                pass

    def _cmd_uw(self, cirno, username, args):
        if cirno.wordscramble_answer != "":
                cirno.sendmsg('%s = %s' % (cirno.wordscramble, cirno.wordscramble_answer))
                cirno.wordscramble_answer= ""
                cirno.wordscramble=""
                cirno.meaning=""
                cirno.wslen=0
                cirno.clue=0
        else:
                cirno.sendmsg('%s: Nothing to answer :doublef' % (username))

    def _cmd_sc(self, cirno, username, args):
        if cirno.wordscramble_answer != "":
                cirno.clue=cirno.clue+1
                if cirno.clue > cirno.wslen:
                    cirno.sendmsg('%s: Fucktard, word is complete :doublef' % (username))
                    return
                clue=cirno.wordscramble_answer[0:cirno.clue]
                #a=dictionary.meaning(cirno.wordscramble_answer)
                #for i in a:
                #    cirno.sendmsg('Scrambled Clue: (%s) -> %s' % (i, a[i][0]))
                #    break
                cirno.sendmsg('Scrambled clue: %s = %s' % (cirno.wordscramble, clue))

    def _cmd_sm(self, cirno, username, args):
        if cirno.wordscramble_answer != "":
                for i in cirno.meaning:
                    cirno.sendmsg('Scrambled Clue: (%s) -> %s' % (i, cirno.meaning[i][0]))
                    break


def setup():
    global words_list
    return Word_Scramble()
