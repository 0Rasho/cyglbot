import random
import os
import urllib
import re
from bs4 import BeautifulSoup

facts_list=[]
class Trivia(object):
    def _cmd_f(self, cirno, username, args):
        global facts_list
        #print "factss ....", facts_list
        if len(facts_list):
                fact = random.choice (facts_list)
                facts_list.remove(fact)
                if not len(facts_list):
                        self.update_facts()
                cirno.sendmsg("Random fact: "+ fact)
        else:
                self.update_facts()
                #print facts_list
                if len(facts_list):
                        fact = random.choice (facts_list)
                        facts_list.remove(fact)
                        if not len(facts_list):
                                self.update_facts()
                        cirno.sendmsg("Random fact: "+ fact)

    def update_facts(self):
                global facts_list
                try:
                        content=urllib.request.urlopen("http://randomfactgenerator.net/").read()
                except:
                        return
                soup = BeautifulSoup(content, "html.parser")
                tdivs = soup.findAll("a", { "class" : "twitter-share-button" })
                max_t=len(tdivs)
                i= 0
                while i < max_t:
                        fact = tdivs[i]['data-text']
                        if len(fact):
                                facts_list.append(fact)
                        i += 1
def setup():
    return Trivia()
