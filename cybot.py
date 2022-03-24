#!/usr/bin/python
# coding: utf-8
# encoding=utf8  

"""
Cyclient bot

Usage: 
    cyclient.py [options]

Options: 
    --room=ROOM           Room to join 
    --name=NICK           Bot nickname 
    --pass=pass           Bot password 
    --files=pass           Bot password 
    --ec=1                 enable commands
    --ab=1                 enable auto bot
"""

from lib.cirno import Cirno
from lib.config import config
import socket
import lib.socks
import datetime
#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9099)
#socket.socket = socks.socksocket
from socketIO_client_nexus import SocketIO
import requests
from threading import Timer
import signal
import sys
import threading
#import magic
import os
import time
import pickle
from docopt import docopt
import random
import urllib
from bs4 import BeautifulSoup
import sys

#reload(sys)
#sys.setdefaultencoding('utf8')


Channel=None
UserName=None
Password=None
maxfiles=0

def cy_disconnect():
    print ("[socket.io disconnect] ")
    global log_update
    try:
         log_update.cancel()
    except:
          pass
    sys.exit()

def cy_error(self, data):
    print ("[socket.io error] ")
    global log_update
    try:
         log_update.cancel()
    except:
          pass
    sys.exit()

class Connections(object):
    def __init__(self):
        self.host = config['Server']['domain']
        if Channel != None:
            config['Server']['channel'] = Channel
        self.channel = config['Server']['channel']
        self.channelpw = config['Server']['channelpass']
        if UserName != None:
                config['Server']['login'] = UserName
        self.name = config['Server']['login']
        if Password != None:
                config['Server']['password'] = Password
        self.password = config['Server']['password']

    def get_socket_config(self):
        url = 'http://%s/socketconfig/%s.json' % (self.host, self.channel)
        req = requests.get(url)
        req=req.json()['servers']
        serv = [i['url'] for i in req if i['secure'] is False][0]
        return serv.rsplit(':', 1)

    def cirnoconnect(self):
        socket_conf = self.get_socket_config()
        host = socket_conf[0]
        port = socket_conf[1]
        print ("%s: Connecting to host %s and channel %s ... \n" %(port, host, socket_conf))
        with SocketIO(host, port, Cirno) as socketIO:
            print ("%s: Connecting to host %s and channel %s ... \n" %(self.name, self.host, self.channel))
            self.socketIO=socketIO
            self.Cirno = self.socketIO._namespace_by_path['']
            self.Cirno.gui = self.gui
            socketIO.on ('disconnect', cy_disconnect)
            socketIO.on ('error', cy_error)
            socketIO.emit('initChannelCallbacks')
            socketIO.emit('joinChannel', {'name': self.channel,
                                          'pw': self.channelpw})
            socketIO.emit('login', {'name': self.name,
                                    'pw': self.password})
            socketIO.wait()

def Kickanons(cirno):
        global anon_kick_time
        anon_kick = Timer(anon_kick_time, Kickanons, [cirno])
        cirno.socketIO.emit('chatMsg', {'msg': "/kickanons", 'meta': {"modflair": 3 }})
        anon_kick.start()

def readlog(cirno):
        return
        global log_update
        log_update = Timer(600, readlog, [cirno])
        cirno.socketIO.emit("readChanLog", {})
        log_update.start()

def input_thread ():
        global cirno
        global anon_kick
        global anon_kick_time
        enable_chat=1
        anon_kick_time=90
        time.sleep(15)
        cirno.stop_tom = 0
        cirno.insult = ''
        #anon_kick = Timer(anon_kick_time, Kickanons, [cirno])
        #anon_kick.start()
        while True:
                line = input("\033[34m"+ cirno.name+" #> "+"\033[0m")
                if len(line) > 0 and enable_chat == 1:
                #if len(line) > 0 and enable_chat == 1:
                    try:
                            if line == "/dc":
                                enable_chat = 0
                                continue
                            elif line == "/ec":
                                enable_chat = 1
                                continue
                            elif line == "/ak":
                                anon_kick = Timer(anon_kick_time, Kickanons, [cirno])
                                anon_kick.start()
                                continue
                            elif line == "/kt":
                                anon_kick_time=int(input("Enter time in seconds: "))
                                continue
                            elif line == "/ck":
                                anon_kick.cancel()
                                continue
                            elif line == "/au":
                                user= input("enter name : ")
                                if len(user) > 0:
                                        config['autousers'].append(user.lower())
                                continue
                            elif line == "/du":
                                user= input("enter name : ")
                                if len (user) > 0:
                                        config['autousers'].remove(user.lower())
                                continue
                            elif line == "/lu":
                                print(config['autousers'])
                                continue
                            elif line == "/rl":
                                cirno.socketIO.emit("readChanLog", {})
                                continue
                            elif line == "/al":
                                user= input("Enter Username: ")
                                cirno.socketIO.emit("assignLeader", { "name": name })
                                continue
                            elif line == "/cls":
                                user= input("Enter Username: ")
                                if len(user) > 1:
                                    css=cirno.Cirno.css+"\n.chat-msg-"+user+"\n{\ndisplay: none;\n}"
                                    cirno.Cirno.css_updated=1
                                    cirno.socketIO.emit("setChannelCSS", { "css": css})
                                continue
                            elif line == "/pm":
                                user= input("Enter Username: ")
                                if len(user) == 0:
                                    continue
                                while True:
                                    msg= input("PM ("+user+") > ")
                                    if msg == "/exit":
                                        break;
                                    if len(msg) == 0:
                                        continue
                                    jmsg={ "to": user, "msg": msg, "meta": {} } 
                                    cirno.socketIO.emit("pm", jmsg)
                                continue
                            elif line == "/ucls":
                                user= input("Enter Username: ")
                                string_2_remove="\n.chat-msg-"+user+"\n{\ndisplay: none;\n}"
                                css=cirno.Cirno.css
                                css=css.replace(string_2_remove, '')
                                cirno.Cirno.css_updated=1
                                cirno.socketIO.emit("setChannelCSS", { "css": css})
                                continue
                            elif line == "/pv":
                                U=cirno.Cirno.userplaylist
                                for u in  U:
                                    print("[ %4d ] ->  %s " %(u, U[u]['title']))
                                videoid= int(input("Enter video id: "))
                                cirno.socketIO.emit("jumpTo", videoid)
                                cirno.socketIO.emit("setCurrent", videoid)
                                cirno.socketIO.emit("changeMedia", U[u])
                                continue
                            elif line == "/da":
                                #[ "setTemp", { "uid": 183, "temp": false } ] 
                                while 1:
                                    U=cirno.Cirno.userplaylist
                                    if len(U) < 10:
                                        break;
                                    try:
                                        for u in  U:
                                            print("[ %4d ] ->  %s " %(u, U[u]['title']))
                                            cirno.socketIO.emit("delete", u )
                                            time.sleep(0.2)
                                    except:
                                          print("errror ....", u)
                                continue

                            elif line == "/dv":
                                #[ "setTemp", { "uid": 183, "temp": false } ] 
                                U=cirno.Cirno.userplaylist
                                for u in  U:
                                    print("[ %4d ] ->  %s " %(u, U[u]['title']))
                                videoid= int(input("Enter video id: "))
                                prev=None
                                nvideoid=None
                                for u in  U:
                                    if prev == videoid:
                                        nvideoid=u
                                        break
                                    prev=u

                                if nvideoid == None:
                                    nvideoid = list(U)[0]

                                print (nvideoid, videoid)

                                cirno.socketIO.emit("delete", videoid )
                                continue

                            elif line == "/p":
                                U=cirno.Cirno.userplaylist
                                for u in  U:
                                    print("[ %4d ] ->  %s " %(u, U[u]['title']))
                                continue

                            elif line == "/r":
                            #[ "setUserRank", { "name": "gLBot", "rank": 1 } ]
                                user= input("Enter Username: ")
                                rank= int(input("Enter Rank to set: "))
                                cirno.socketIO.emit("setUserRank", { "name": user, "rank": rank })
                                continue
                            elif line == "/l":
                                U=cirno.Cirno.userdict
                                for u in  cirno.Cirno.userdict:
                                        uptime = time.time() - U[u]['uptime']
                                        uptime = (datetime.timedelta(seconds=round(uptime)))
                                        print("%s [%d] [%s]" %(u, int(U[u]['rank']), uptime))
                                        print ("      Alias: ", U[u]['alias'])
                                        if int(U[u]['lmts']) != 0:
                                                print("      lmts : ", datetime.datetime.fromtimestamp(int(U[u]['lmts'])))
                                        print("      muted: ", U[u]['smuted'])
                                print("Connected users : ", cirno.Cirno.total_users)
                                continue
#                               self.userdict[name] = {
#                                   'rank': rank,
#                                   'afk': afk,
#                                   'uptime': int(time.time()),
#                                   'alias': alias,
#                                   'msg' : collections.deque(maxlen=9),
#                                   'lmts' : 0,   #last msg time stamp 
#                                   'smuted' : 0
#                               }
                    except:
                        print ("cexecp")
                        continue
                    cirno.socketIO.emit('chatMsg',
                              {'msg': line,
                                'meta': {
                                      }
                               })

                
def handle_signal(signum, frame):
        global log_update
        try:
            log_update.cancel()
        except:
            pass
        sys.exit()
def build_chat():
        if maxfiles == 0:
                return
        i = 0
        filedir="SRT"
        mime = magic.Magic(mime=True)
        follow={}
        for root, dirs, filenames in os.walk(filedir):
            for f in filenames:
                if f == "robots.txt" or f == "cano.txt":
                        continue
                path = os.path.join(root, f)
                if mime.from_file(path) == 'text/plain' or path.endswith('.txt'):
                        i = i + 1
                        b=open(path)
                        text=[]
                        for line in b:
                            for word in line.split():
                                text.append (word)
                        b.close()
                        textset=list(set(text))
                        for l in range(len(textset)):
                            check=textset[l]
                            try:
                                    a = follow[check]
                            except:
                                     follow[check]=[]

                            for w in range(len(text)-1):
                                if check==text[w] and text[w][-1] not in '(),.?!':
                                    word = str(text[w+1])
                                    if word not in follow[check]:
                                            follow[check].append(word)
                if i == maxfiles:
                    break
            if i == maxfiles:
                break
        a=open(config['AIdatafile'],'wb')
        pickle.dump(follow,a,2)
        a.close()


def start():
    global log_update
    global cirno
    #global userio
    signal.signal(signal.SIGINT, handle_signal)
    #userio = threading.Thread(target=input_thread)
    #userio.setDaemon(True)
    cirno = Connections()
    cirno.gui = None
    #userio.start()
    if UserName != None and Password != None:
        if Channel == "101":
             log_update = Timer(60, readlog, [cirno])
             log_update.start()
    cirno.cirnoconnect()

if __name__ == '__main__':
    global successorlist
    signal.signal(signal.SIGINT, handle_signal)
    args = docopt(__doc__, version='0.1')
    abot = 0
    cmds = 0
    if args['--room']:
        Channel = args['--room']
    if args['--name']:
        UserName = args['--name']
    if args['--pass']:
        Password = args['--pass']
    if args['--files']:
        maxfiles = int(args['--files'])
    if args['--ec']:
        cmds = int(args['--ec'])
    if args['--ab']:
        abot = int(args['--ab'])
    if cmds == 1:
            config['disablecmds'] = False
    if abot == 1:
            config['autobot'] = True
    start()
