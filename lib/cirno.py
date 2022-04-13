from socketIO_client_nexus import BaseNamespace
from lib.database import CirnoDatabase
import re
import urllib
from lib.utils import *
from lib.commands import *
from lib.config import config
import random
import pickle
import time
import collections
import datetime

joined_chat=False
successorlist=None
def nextword(a):
    global successorlist
    if successorlist == None:
        a=open(config['AIdatafile'],'rb')
        successorlist=pickle.load(a)
        a.close()
    try:
            return random.choice(successorlist[a]).lower()
    except:
                return '.?'
    else:
        return '.?'

def remove_tags(text):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', text)
class Cirno(BaseNamespace):
    def __init__(self, io, path):
        super(Cirno, self).__init__(io, path)
        self.db = CirnoDatabase(config['Server']['channel'])
        self.starttime = int(time.time() * 1000)
        self.cirnostart = time.time()
        self.pm_cmd_usr=None
        self.pm_cmd=None
        self.current_vid=None
        self.play_this_video=None
        self.userdict = {}
        self.stop_new_chats=0
        self.kick_new_chats=0
        self.css=None
        self.css_updated=0
        self.cmdthrottle = {}
        self.total_users = 0
        self.settings = {'disallow': []}
        self.channelOpts = {}
        self.userplaylist={}
        self.emotelist={}
        self.emupdatef=open('db/emotes-'+str(config['Server']['channel'])+'.mod', 'a+')
        self.rank = 0
        self.trivia_answer = ""
        self.trivia_opt=""
        self.wordscramble_answer = ""
        self.wordscramble = ""
        loadplugins()
        updatesettings(self)
        self.allowed_sources = config['Misc']['allowed_sources']
        self.what = config['Misc']['errorpic']
        self.name = config['Server']['login']
        self.mod = config['Server']['modflair']
        self.disallowed2ch = config['API']['disallow_2ch_boards'].split()
        self.disallowed4ch = config['API']['disallow_4chan_boards'].split()

    def cy_print(self, username, msg):
        if self.gui == None:
            return
            print(msg)
        else:
            if username == "":
                self.gui._insert_message(self.gettime()+msg, "")
            else:
                self.gui._insert_message(msg, username)

    def on_login (self, data):
        status = data['success']
        if status == True:
                username = data['name']
                self.cy_print("", username+ " logged in successfully ...")
        else:
                self.cy_print ("","Failed to login : "+ data['error'])

    def on_removeEmote(self, data):
        self.emupdatef.write("DEL "+str(data['name'])+" "+str(data['image'])+"\n")
        del self.emotelist[data['name']]

    def on_updateEmote(self, data):
        self.emupdatef.write("ADD "+str(data['name'])+" "+str(data['image'])+"\n")
        self.emotelist[data['name']]=1

    def on_setMotd(self, data):
        self.db.insertmotd(data)

    def on_emoteList (self, data):
        for i in data:
            self.emotelist[i['name']]=1
        f=open('db/emotes-'+str(config['Server']['channel'])+'.update', 'w')
        f.write(str(data))
        f.close()

    def on_usercount (self, data):
        self.total_users = data

    def on_chatMsg(self, data):
        timestamp = data['time']
        #print timestamp, datetime.datetime.utcfromtimestamp(timestamp / 1e3)
        username = data['username']
        msg = data['msg']
        meta = data['meta']
        n_times=0

        timestr=(time.strftime("[%F %T] ", time.gmtime(timestamp / 1e3)))
        if username == '[server]':
            buf="\033[31m\033[01m"+ msg + "\033[0m"
            #if "kicked" in msg:
            #    self.sendmsg(msg)
            if self.gui == None:
                print(buf)
            else:
                self.cy_print(timestr+username, msg)
            return

        msg = filterchat(msg)
        if msg is None:
            return

        self.db.insertchat(timestamp, username, msg)
        chat_msg=("\033[31m\033[01m%s |\033[34m\033[01m %12s\033[0m : \033[32m%s\033[0m" \
                % (str(datetime.datetime.utcfromtimestamp(int(timestamp / 1e3))), username, msg))
        if self.gui == None:
            print(chat_msg)
        else:
            self.cy_print(timestr+username, msg)

        if timestamp < self.starttime:
            return

        if config['disablecmds'] == False and msg.startswith('!') \
                and 'shadow' not in meta \
                and username not in readsettings()["disallow"]:
             handle(self, username, msg)

        timediff = -1
        timestamp = timestamp / 1e3

        try:
                #if msg.startswith('!'):
                #    msg=msg.split(' ')[0]
                self.userdict[username]['msg'].append(msg)
                if self.userdict[username]['lmts'] != 0:
                        timediff = timestamp - self.userdict[username]['lmts']
                self.userdict[username]['lmts'] = timestamp
        except:
                pass

        if self.userdict[username]['smuted'] == 1 and 'shadow' not in meta:
                self.userdict[username]['smuted'] = 0

        try:
            msg1 = remove_tags(msg)
            emotes=msg1.split()
            n_w={}
            for e_m in emotes:
                if e_m.startswith(":") or e_m.startswith("\\") or e_m.startswith("/"):
                    if e_m.startswith(":"):
                        try:
                            is_emote=self.emotelist[e_m]
                        except KeyError:
                            try:
                                self.get_update_mfc_emote_link(e_m)
                            except:
                                continue
                    if e_m != "/></a>":
                        self.db.insert_emote(e_m)
                        self.db.insert_uemote(username, e_m)
                else:
                    if len(e_m) > 3:
                        self.db.insert_uword(username, e_m)
                try:
                    n_w[e_m] += 1
                except:
                    n_w[e_m] = 1
                    pass
            s_n_w=sorted(n_w.items(), key=lambda x: x[1], reverse=True)

            n_times=s_n_w[0][1]
            n_string=s_n_w[0][0]
        except:
            pass

        if n_times >= 8:
            same_emote=0
            if n_string[0] == ":" and len(n_string) > 1:
                same_emote=1
            if same_emote == 1 or "https://" in n_string or "http://" in n_string or "www:" in n_string:
                if self.rank >= 3 and self.name.lower() != username.lower():
                        self.sendmsg("/smute "+username)
                        self.uclear_chat(username, 1)
                        self.userdict[username]['smuted']  = 1
                        self.sendmsg("/kick "+username+ " Pussy, Create your own room and SPAM. See ya!. x _|_ x")

        if len(self.userdict[username]['msg']) == 10 and \
           self.userdict[username]['msg'].count(msg) >= 6 and  \
           self.name.lower() != username.lower():
                if self.userdict[username]['smuted'] == 0:
                        self.sendmsg("/kickanons")
                        self.sendmsg("/smute "+username)
                        self.uclear_chat(username, 1)
                        self.userdict[username]['smuted']  = 1
                        #self.sendmsg("/kick "+username+ " - Kicked for spamming")
                        #self.sendmsg("Kicked "+ username+" for spamming")
                        print("\033[31m\033[01m******Cleared "+ username + " ************* \033[0m")

        if int(timediff) > 30:
                self.userdict[username]['msg'].clear()
                if self.userdict[username]['smuted'] == 1 and self.stop_new_chats == 0:
                    self.sendmsg("/unmute "+username)
                    self.uclear_chat(username, 0)

    def on_pm(self, data):
        username = data['username']
        msg = data['msg']
        rank = self.db.getuserrank(username)

        self.cy_print("[*PM*] "+ username, msg)

        timestamp = int(time.time() * 1000)
        self.db.insertchat(timestamp, username, " [*PM*] "+msg)
        msg = filterchat(msg)
        if msg is None:
            return
        rval=handle_pm_cmds(self, username, msg)
        self.pm_cmd=None
        self.pm_cmd_usr=None
        return rval

    def get_update_mfc_emote_link(self,ecode):
        mfc_url_pcs="https://www.myfreecams.com/mfc2/php/ParseChatStream.php?"
        name=ecode
        if name[0] == ':':
            name=name[1:]
        e_http=mfc_url_pcs+"a0="+str(name)+"&"+"&"+str(random.random())
        response=str(urllib.request.urlopen(e_http).read())[4:-3]
        emote = dict(response.split(':"') for response in response.split(',"'))
        url=str(emote['url"']).replace('\\','').strip('"')
        if not "broken.gif" in url:
            mmsg={"name":":"+str(name.strip()),"image":str(url)}
            self.sendraw("updateEmote", mmsg)
            self.sendmsg(':%s' % (str(name.strip())))
            self.emotelist[ecode]=1

    def on_addUser(self, data):
        name = data['name']
        rank = data['rank']
        afk = data['meta']['afk']
        ip = None
        try:
            ip  = data['meta']['ip']
        except:
            ip = None
            pass
        try:
                alias = data['meta']['aliases']
        except:
                alias = None

        self.cy_print ("", "Joined : "+name+" ("+str(ip)+") alias: "+str(alias))
        self.userdict[name] = {
            'rank': rank,
            'afk': afk,
            'uptime': int(time.time()),
            'alias': alias,
            'msg' : collections.deque(maxlen=20),
            'lmts' : 0,   #last msg time stamp 
            'smuted' : 0,
            'ip' : ip
        }
                
        if name == self.name:
            config['Iamjoined'] = True
        else:
            if rank < 2 and self.stop_new_chats == 1:
                self.sendmsg("/smute "+name)
                self.userdict[name]['smuted']  = 1
            if rank < 2 and self.kick_new_chats == 1:
                self.sendmsg("/kick "+name+ " See ya!. Create your own room")
        self.db.insertuser(name, rank)
        if ip != None:
            self.db.insertuserip(name, ip)
        self.db.insertuserrank(name, rank)

    def on_channelOpts(self, data):
        self.channelOpts = data

    def gettime(self):
        timestr=(time.strftime("[%F %T] ", time.gmtime(int(time.time()))))
        return timestr

    def on_userLeave(self, data):
        name=data['name']
        self.cy_print("", name + " has left ")
        del self.userdict[name]

    def on_channelOpts(self, data):
        self.channelOpts = data

    def on_userlist(self, data):
        for i in data:
            try:
                alias = i['meta']['aliases']
            except:
                alias = ""
            name=i['name']
            rank=i['rank']
            try:
                ip=i['meta']['ip']
            except:
                ip=None
            self.userdict[i['name']] = {
                'rank': i['rank'],
                'afk': i['meta']['afk'],
                 'uptime': int(time.time()),
                 'alias': alias,
                 'msg' : collections.deque(maxlen=20),
                 'lmts' : 0,   #last msg time stamp,
                 'smuted' : 0
            }

            if self.name.lower() == i['name'].lower():
                self.rank = i['rank']

            if rank < 2 and self.stop_new_chats == 1:
                self.sendmsg("/smute "+name)
                self.userdict[name]['smuted']  = 1

            if ip != None:
                self.db.insertuserip(name, ip)

    def on_setAFK(self, data):
        username = data['name']
        afk = data['afk']
        if username and data:
            self.userdict[username]['afk'] = afk

    def openpoll(self, data):
        self.emit('newPoll', data)

    def sendraw(self, mtype,  message):
        self.emit(mtype, message)

    def sendmsg1(self, message):
        if self.pm_cmd_usr != None:
            jmsg={ "to": self.pm_cmd_usr, "msg": message, "meta": {} } 
            self.emit("pm", jmsg)
            self.pm_cmd=None
            self.pm_cmd_usr=None
            return
        if self.mod:
            self.emit('chatMsg',
                      {'msg': message,
                       'meta': {
                           "modflair": 3
                       }
                       })
        else:
            self.emit('chatMsg',
                      {'msg': message,
                       'meta': {}
                       })


    def sendmsg(self, message):
        if self.pm_cmd_usr != None:
            jmsg={ "to": self.pm_cmd_usr, "msg": message, "meta": {} } 
            self.emit("pm", jmsg)
            self.pm_cmd=None
            self.pm_cmd_usr=None
            return
        rank = self.db.getuserrank(self.name)
        if self.mod:
            self.emit('chatMsg',
                      {'msg': message,
                       'meta': {
                           "modflair": rank
                       }
                       })
        else:
            self.emit('chatMsg',
                      {'msg': message,
                       'meta': {}
                       })

    def handle_voteskip(self):
        if self.channelOpts['allow_voteskip']:
            self.emit('setOptions', {'allow_voteskip': False})
        else:
            self.emit('setOptions', {'allow_voteskip': True})

    def on_queue(self, data):
#{u'item': {u'media': {u'title': u'Pink Floyd - Marooned (Official Music Video)', u'seconds': 326, u'meta': {}, u'duration': u'05:26', u'type': u'yt', u'id': u'P7YMI39sObY'}, u'uid': 127, u'temp': True, u'queueby': u'Melipal'}, u'after': 126}

#{u'title': u'Pink Floyd - Marooned (Official Music Video)', u'seconds': 326, u'currentTime': 0, u'paused': False, u'meta': {}, u'duration': u'05:26', u'type': u'yt', u'id': u'P7YMI39sObY'}
        username = data['item']['queueby']
        uid = data['item']['uid']
        dur=data['item']['media']['duration']
        secs=data['item']['media']['seconds']
        title=data['item']['media']['title']
        ty=data['item']['media']['type']
        v_id=data['item']['media']['id']
        meta=data['item']['media']['meta']

        emitmsg={'title': title, 
                'seconds': secs, 
                'currentTime': 0, 
                'paused': False, 
                'meta': meta, 
                'duration': dur, 
                'type': ty, 
                'id': v_id}
        try:
                self.userplaylist[uid] = emitmsg
        except:
                self.userplaylist[uid]= emitmsg
        buf = "%s added \"%s\" duration %s" % (username, title, dur)
        self.cy_print("", buf)
        if self.play_this_video == v_id:
            self.emit("jumpTo", uid)
            self.emit("setCurrent", uid)
            self.emit("changeMedia", emitmsg)
            self.play_this_video=None
        timestamp = int(time.time() * 1000)
        self.db.insertchat(timestamp, username, "Added video \""+ title+"\"")

    def on_delete(self, data):
        uid = data['uid']
        try:
            title=self.userplaylist[uid]['title']
            buf="%s titled video has been deleted" % (title)
            self.cy_print("", buf)
            del self.userplaylist[uid]
        except:
            pass
        return
        for i in self.userplaylist:
                try:
                        title=self.userplaylist[i][uid][0]
                        del self.userplaylist[i][uid]
                        buf="%s's video %s has been deleted" % (i, title)
                        self.cy_print("", buf)
                except:
                        pass

    def on_changeMedia(self, data):
        self.current_vid=data['id']
        id=data['id']
        title=data['title']
        type=data['type']
        dur=data['seconds']
        buf="Playing : %s  - duration %s" % (data['title'], data['duration'])
        self.db.insert_media(id, title, type, dur)
        self.cy_print("", buf)


    def on_channelCSSJS(self, data):
        self.css=data['css']
        timestamp = int(time.time() * 1000)
        self.db.insertcss(data['cssHash'], timestamp, self.css)

    def on_setCurrent(self, data):
        self.current_vid=data

    def on_readChanLog(self, data1):
        d=data1['data']
        for i in d.split('\n'):
            try:
                if "[login]" in i:
                    self.db.insert_login(i)
                elif "[mod]" in i:
                    timestamp = int(time.time() * 1000)
                    self.db.insert_mod(i, timestamp)
                elif "[playlist]" in i:
                    self.db.insert_pl(i)
                elif "[init]" not in i:
                    self.db.insert_chatlog(i)
            except:
                pass
        self.db.conn.commit()
    def on_playlist(self, data1):
        for data in data1:
            username = data['queueby']
            uid = data['uid']
            dur=data['media']['duration']
            secs=data['media']['seconds']
            title=data['media']['title']
            ty=data['media']['type']
            v_id=data['media']['id']
            meta=data['media']['meta']

            emitmsg={'title': title, 
                    'seconds': secs, 
                    'currentTime': 0, 
                    'paused': False, 
                    'meta': meta, 
                    'duration': dur, 
                    'type': ty, 
                    'id': v_id}
            try:
                    self.userplaylist[uid] = emitmsg
            except:
                    self.userplaylist[uid]= emitmsg
            self.db.insert_playlist(str(ty)+"/"+str(v_id), title)
        return
        for arg in args:
            for media in arg:
                if 'media' in media:
                    if media['media']['id'] not in self.media:
                        self.media.append(media['media']['id'])
        log.info('Playlist Loaded')

    def tab_spam(self, val):
        self.stop_new_chats=val

    def kick_spam(self, val):
        self.kick_new_chats=val


    def uclear_chat(self, username, clear):
        string_ar="\n.chat-msg-"+username+"\n{\ndisplay: none;\n}"
        css=self.css
        if clear == 1:
            css=css+string_ar
        else:
            css=css.replace(string_ar, '')
        self.css_updated=1
        self.emit("setChannelCSS", { "css": css})

    def control_spam(self, username, clear):
        spam="\n.chat-msg-"+username+" .username { text-transform: capitalize; }.chat-msg-"+username+" {  text-transform: lowercase; !important} .chat-msg-"+username+" a { visibility: hidden; font-size:0;  } .chat-msg-"+username+" a:before { visibility: visible; content: 'LINK'; font-size:initial;color: inherit;text-decoration: underline; } .chat-msg-"+username+" img { height: 50px;      width: 50px;  }"
        css=self.css
        if clear == 1:
            css=css+spam
        else:
            css=css.replace(spam, '')
        self.css_updated=1
        self.emit("setChannelCSS", { "css": css})

    def addvideo(self, play,  typev, idv, duration, temp, pos, link):
        if link:
            json = {
                'id': link['id'],
                'type': link['type'],
                'pos': pos,
                'duration': duration,
                "temp": temp
            }
            self.emit("queue", json)
            if play == 1:
                self.play_this_video=link['id']
            if config['Server']['login'].lower() == 'aspen':
                timestamp = int(time.time() * 1000)
                self.db.insertchat(timestamp, "MEDIA", str(link['type'])+".com/"+str(link['id']))
        else:
            json = {
                'id': idv,
                'type': typev,
                'pos': pos,
                'duration': duration,
                "temp": temp
            }
            self.emit("queue", json)
        time.sleep(1)
