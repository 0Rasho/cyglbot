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
from lib.motd import *
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
import os
import time
import pickle
from docopt import docopt
import random
import urllib
from bs4 import BeautifulSoup
import sys
import base64
import json

Channel=None
UserName=None
Password=None

def cy_disconnect():
    print ("[socket.io disconnect] ")
    os._exit(0)

def cy_error(self, data):
    print ("[socket.io error] ")
    os._exit(0)

def handle_signal(signum, frame):
    os._exit(0)

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

def gifs_update():
    code = b'TElWRFNSWlVMRUxB'
    gcache = open('db/cache', 'r')
    gcache.seek(0, os.SEEK_SET)
    gifs=[]
    for link in gcache:
        link=link.strip('\n')
        link=link.strip()
        gifs.append(link)
    gcache.close()
    gcache = open('db/cache', 'a')
    while True:
        lmt = 64
        search = [ b'Ym9vYnM=', b'dGl0cw==', b'c2V4eSBnaXJscw==', b'YmlraW5p', b'Z2lybHMga2lzc2luZw==', b'bGVzYmlhbg==' ]
        for search_term in search:
            search_term = base64.b64decode(search_term).decode('utf-8')
            r = requests.get(
                "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, code.decode('utf-8'), lmt))
            if r.status_code == 200:
                top_8gifs = json.loads(r.content)
                results = top_8gifs["results"]
                for res in results:
                    url=res["media"][0]["mediumgif"]["url"]
                    if url not in gifs:
                        gifs.append(url)
                        gcache.write(url)
                        gcache.write("\n")
            time.sleep(300)
        time.sleep(7200)

def update_motd(cirno):
    cirno.motd.get_updated_news()
    motd = cirno.motd.get_motd()
    cirno.socketIO.emit("setMotd", { "motd": str(motd) })

def evtthread(cirno):
    time.sleep(60)
    cirno.motd_itr = 0
    update_motd(cirno)

    motdeintr=60
    logintr=10
    tintr = 0

    while True:
        time.sleep(120)
        tintr += 2
        if tintr % motdeintr == 0:
            update_motd(cirno)
        if tintr % logintr == 0:
            cirno.socketIO.emit("readChanLog", {})

def start():
    global cirno
    signal.signal(signal.SIGINT, handle_signal)
    cirno = Connections()
    cirno.gui = None
    cirno.motd = MOTD()

    if UserName != None and Password != None:
        tgif = threading.Thread(target=gifs_update, daemon=True)
        tgif.start()

        evtthr = threading.Thread(target=evtthread, args=[cirno], daemon=True)
        evtthr.start()

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
    if args['--ec']:
        cmds = int(args['--ec'])
    if cmds == 1:
            config['disablecmds'] = False
    start()
