import random
import os

rudy_quotes=[]
bruce_quotes=[]
fe=[]
class RudyQuotes(object):
    def update_rudy_quotes(self):
        global rudy_quotes
        global fe
        try:
                file1 = open('db/rquotes', 'r')
                file1.seek(0, os.SEEK_SET)
                for quote in file1:
                        quote=quote.strip('\n')
                        quote=quote.strip()
                        rudy_quotes.append(quote)
                rudy_quotes.shuffle()
                rudy_quotes.shuffle()
                rudy_quotes.shuffle()
                file1.close()
        except:
                pass
        try:
                file1 = open('db/fe.txt', 'r')
                file1.seek(0, os.SEEK_SET)
                for quote in file1:
                        quote=quote.strip('\n')
                        quote=quote.strip()
                        fe.append(quote)
                fe.shuffle()
                fe.shuffle()
                fe.shuffle()
                file1.close()
        except:
                pass

    def _cmd_r(self, cirno, username, args):
        global rudy_quotes
        if len(rudy_quotes) == 0:
                self.update_rudy_quotes()
        try:
                r_fact= rudy_quotes.pop(random.randint(0, len(rudy_quotes)-1))
                cirno.sendmsg(r_fact)
        except:
                pass
    def update_bruce_quotes(self):
        global bruce_quotes
        global fe
        try:
                file1 = open('db/bruce', 'r')
                file1.seek(0, os.SEEK_SET)
                for quote in file1:
                        quote=quote.strip('\n')
                        quote=quote.strip()
                        bruce_quotes.append(quote)
                bruce_quotes.shuffle()
                bruce_quotes.shuffle()
                bruce_quotes.shuffle()
                file1.close()
        except:
                pass

    def _cmd_b(self, cirno, username, args):
        global bruce_quotes
        if len(bruce_quotes) == 0:
                self.update_bruce_quotes()
        try:
                r_fact= bruce_quotes.pop(random.randint(0, len(bruce_quotes)-1))
                cirno.sendmsg(r_fact)
        except:
                pass

    def _cmd_fe(self, cirno, username, args):
        global fe
        if len(fe) == 0:
                self.update_rudy_quotes()
        try:
                r_fact= fe.pop(random.randint(0, len(fe)-1))
                cirno.sendmsg(r_fact)
        except:
                pass

def setup():
    global rudy_quotes
    return RudyQuotes()
