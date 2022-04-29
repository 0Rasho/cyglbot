from time import time
from datetime import timedelta
from random import choice, randint, uniform
import random
from lib.utils import checkrank
import giphypop
from lib.utils import throttle
from PyDictionary import PyDictionary
import wikipedia
import requests
import sys
import socket
import urllib
import os
import json

dictionary=PyDictionary()
g = giphypop.Giphy()
offset=0

import lib.socks as socks
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9099)


pruser= []

def get_gif_list(last_offset, key, limit):
    return None
    params = {'q': (key)}
    params['api_key'] = ""
    params['limit'] = limit
    params['offset'] = last_offset
    resp = requests.get("http://api.giphy.com/v1/gifs/search", params=params)
    k=(resp.json())
    try:
        k= k['data']
    except:
        pass
    i=0
    glist=[]
    while i < len(k):
        try:
            url=str(k[i]['images']['fixed_width']['url'].split('?')[0])
            glist.append(url)
        except:
            pass
        i=i+1
    return glist

class BasicCommands(object):
    @throttle(300)
    def _cmd_btc(self, cirno, username, args):
        import requests
        bitcoin_api_url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
        response = requests.get(bitcoin_api_url)
        r = response.json()
        name=r['chartName']
        usd=r['bpi']['USD']['rate']
        eur=r['bpi']['EUR']['rate']
        cirno.sendmsg('%s: %s = %s USD  %s EUR' % (username, name, usd, eur))

    @throttle(15)
    def _cmd_g(self, cirno, username, args):
        if args:
            code = b'TElWRFNSWlVMRUxB'
            lmt = 16
            search_term = str(args)
            r = requests.get(
                "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, code.decode('utf-8'), lmt))
            if r.status_code == 200:
                top_8gifs = json.loads(r.content)
                results = top_8gifs["results"]
                ngifs = len(results)
                url=results[random.randint(0, ngifs)]["media"][0]["mediumgif"]["url"]
                cirno.sendmsg('%s' % (url))

    def _cmd_uptime(self, cirno, username, args):
        uptime = time() - cirno.cirnostart
        uptime = '%s' % (timedelta(seconds=round(uptime)))
        cirno.sendmsg('%s: Online: %s' % (username, uptime))

    def _cmd_pick(self, cirno, username, args):
        values = args.split(' ')
        if len(values) > 1:
            cirno.sendmsg('%s: %s' % (username, choice(values)))
        else:
            cirno.sendmsg('%s: Choose at least two options.' % username)

    def _cmd_k(self, cirno, username, args):
        try:
                #rank = int(cirno.userdict[username]['rank'])
                #if rank >= 2:
                '''
                if args:
                    msg1={"msg": "/kick "+str(args)+" "+str(username)+"  kicked you! :( ", "meta": {}}
                else:
                    msg1={"msg": "/kickanons", "meta": {}}
                '''
                msg1={"msg": "/kickanons", "meta": {}}
                cirno.sendraw("chatMsg", msg1)
        except:
                pass
    def _cmd_roll(self, cirno, username, args):
        randoften = randint(0, 10)
        if args and args.isdigit():
            setrand = randint(0, int(args))
            cirno.sendmsg('%s: %s' % (username, setrand))
        else:
            cirno.sendmsg('%s: %s' % (username, randoften))

    def _cmd_rate(self, cirno, username, args):
        name = args.split()[0]
        name = name.lower()
        rating=0.0
        if name:
            rating=round(uniform(1.0,9.5),1)
            cirno.sendmsg('%s: rating %s/10' % (name, str(rating)))

    def _cmd_n(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Enter your search!' % username)
        else:
            for user in cirno.userdict.keys():
                if user.lower() == args.lower():
                        cirno.sendmsg('%s => %s' % (args, ",".join(str(x) for x in cirno.userdict[user]['alias'])))

    def send_gif(self, cirno, username, args, count):
            offset=choice([0,25,50])
            #limit=random.choice([25,50,75,100])
            limit=100
            results=get_gif_list(offset,"\""+args+"\"", limit)
            if len(results)==0:
                results=get_gif_list(0,"\""+args+"\"", 25)
            i=0
            while i < count:
                url=results[(random.randrange(0, len(results)-1))]
                i=i+1
                user=cirno.pm_cmd_usr
                cirno.sendmsg('%s' % (url))
                cirno.pm_cmd_usr=user
            cirno.pm_cmd_usr = None

    def _cmd_g3(self, cirno, username, args):
        if args:
            self.send_gif(cirno, username, args, 3)

    def _cmd_g2(self, cirno, username, args):
        if args:
            self.send_gif(cirno, username, args, 2)

    def _cmd_g4(self, cirno, username, args):
        if args:
            self.send_gif(cirno, username, args, 4)

    def _cmd_g5(self, cirno, username, args):
        if args:
            self.send_gif(cirno, username, args, 5)

    def _cmd_g6(self, cirno, username, args):
        if args:
            self.send_gif(cirno, username, args, 6)

    def _cmd_g7(self, cirno, username, args):
        if args:
            self.send_gif(cirno, username, args, 7)

    def _cmd_g8(self, cirno, username, args):
        if args:
            self.send_gif(cirno, username, args, 8)

    def _cmd_g9(self, cirno, username, args):
        if args:
            self.send_gif(cirno, username, args, 9)


    def _cmd_g10(self, cirno, username, args):
        if args:
            self.send_gif(cirno, username, args, 10)

    def _cmd_gdisable(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Enter your search!' % username)
        else:
            offset=0
            #offset=choice([0,25,50,75,100,125])
            #limit=random.choice([25,50,75,100])
            limit=50
            results=get_gif_list(offset,"\""+args+"\"", limit)
            if len(results)==0:
                results=get_gif_list(0,"\""+args+"\"", 25)
            url=choice(results)
            cirno.sendmsg('%s: %s' % (username, url))

    def _cmd_c(self, cirno, username, args):
        if not args:
            return
        src=args
        math=args.replace('x', '*')
        math=math.replace('X', '*')
        math=math.replace('=', '')
        math=math.replace('+', '%2B')
        api="https://api.mathjs.org/v4/?expr="+math
        res=str(urllib.request.urlopen(api).read())[2:-1]
        if "Error" not in res:
            cirno.sendmsg('%s: %s = %s' % (username, src, res))

    def _cmd_m(self, cirno, username, args):
        if not args:
            return
        mfc_url_pcs="https://www.myfreecams.com/mfc2/php/ParseChatStream.php?"
        if args[0] == ':':
            args=args[1:]
        e_http=mfc_url_pcs+"a0="+str(args)+"&"+"&"+str(random.random())
        response=str(urllib.request.urlopen(e_http).read())[4:-3]
        emote = dict(response.split(':"') for response in response.split(',"'))
        url=str(emote['url"']).replace('\\','').strip('"')
        cirno.sendmsg('%s: %s' % (username, url))
        if not "broken.gif" in url:
            mmsg={"name":":"+str(emote['"txt"'].strip('"')),"image":str(url)}
            cirno.sendraw("updateEmote", mmsg)

    def _cmd_d(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Enter your search!' % username)
            return
        a=dictionary.meaning(args)
        if len(a)==1:
            for i in a:
                cirno.sendmsg('%s: (%s) -> %s' % (args, i, ','.join(map(str, a[i]))))
        elif len(a) > 1:
            for i in a:
                #cirno.sendmsg('%s: (%s) -> %s' % (args, i, ','.join(map(str, a[i]))))
                cirno.sendmsg('%s: (%s) -> %s' % (args, i, a[i][0]))

    def _cmd_w(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Enter your search!' % username)
        else:
            for user in cirno.userdict.keys():
                if user.lower() == args.lower():
                        cirno.sendmsg('%s => %s' % (args, ",".join(str(x) for x in cirno.userdict[user]['alias'])))

    def _cmd_wk(self, cirno, username, args):
        if not args:
            cirno.sendmsg('%s: Enter your search!' % username)
            return
        a=wikipedia.summary("\""+args+"\"", sentences=3)
        import textwrap
        if len(a)>1:
            a=textwrap.fill(a, 160).split('\n')
            j=0
            for i in a:
                user=cirno.pm_cmd_usr
                if j == 0:
                    cirno.sendmsg('%s:  %s' % (args, i))
                    j = 1
                else:
                    cirno.sendmsg('%s' % (i))
                cirno.pm_cmd_usr=user
        cirno.pm_cmd_usr = None

    def _cmd_cls(self, cirno, username, args):
            if username not in pruser:
                return
            name=str(args).replace(" ", '')
            cirno.uclear_chat(name, 1)

    def _cmd_ucls(self, cirno, username, args):
            if username not in pruser:
                return
            name=str(args).replace(" ", '')
            cirno.uclear_chat(name, 0)

    def _cmd_spam(self, cirno, username, args):
            if username not in pruser:
                return
            name=str(args).replace(" ", '')
            cirno.control_spam(name, 1)

    def _cmd_nspam(self, cirno, username, args):
            if username not in pruser:
                return
            name=str(args).replace(" ", '')
            cirno.control_spam(name, 0)

    def _cmd_ff(self, cirno, username, args):
            if username not in pruser:
                return
            cirno.tab_spam(1)

    def _cmd_nff(self, cirno, username, args):
            if username not in pruser:
                return
            cirno.tab_spam(0)

    def _cmd_fo(self, cirno, username, args):
            if username not in pruser:
                return
            cirno.kick_spam(1)

    def _cmd_nfo(self, cirno, username, args):
            if username not in pruser:
                return
            cirno.kick_spam(0)

    def _cmd_e(self, cirno, username, args):
            arg = args.split()
            if len(arg) < 2:
                return
            url=arg[2].split("=")[1].strip('"')
            mmsg={"name":":"+str(arg[0].strip(":")),"image":str(url)}
            cirno.sendraw("updateEmote", mmsg)

    def _cmd_ww(self, cirno, username, args):
            if len(args):
                user=args
            else:
                user=None
            a=cirno.db.get_wusage(user)
            buf=""
            if a == None:
                return
            else:
                for i in a:
                    buf+=str(i[0])+" = "+str(i[1])+ " "
            if user == None:
                cirno.sendmsg('words: %s' % buf)
            else:
                cirno.sendmsg('%s : %s' % (user, buf))

    def _cmd_ui(self, cirno, username, args):
            a=cirno.db.ipdb.get_u2ip(args)
            if a == None:
                return
            buf=""
            a=a.split(',')
            le=len(a)
            j=0
            while le:
                le = le - 1
                buf+=a[le]+" "
                j=j+1
                if j == 5:
                    break;
            cirno.sendmsg('%s : %s:%s' % (username, args, str(buf)))

    def _cmd_ml(self, cirno, username, args):
            a=cirno.db.mediadb.get_media(str(args))
            if a == None:
                return
            cirno.pm_cmd_usr=username
            cirno.sendmsg('%s' % (str(a)))

    def _cmd_eu(self, cirno, username, args):
            if len(args):
                user=args
            else:
                user=None
            a=cirno.db.get_emoteusage(user)
            buf=""
            if a == None:
                return
            else:
                for i in a:
                    buf+=str(i[0])+" = "+str(i[1])+ " "
            print(buf)
            if user == None:
                cirno.sendmsg('emotes: %s' % buf)
            else:
                cirno.sendmsg('%s : %s' % (user, buf))

    @checkrank(2)
    def _cmd_vs(self, cirno, username, args):
        cirno.handle_voteskip()

    @checkrank(5)
    def _cmd_swu(self, cirno, username, args):
            os.system("sudo pip3 install -r requirements.txt; git pull");
            os._exit(0)

    @checkrank(5)
    def _cmd_shutdown(self, cirno, username, args):
            if username not in pruser:
                return
            os._exit(0)



def setup():
    return BasicCommands()
