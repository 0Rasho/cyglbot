import sqlite3

class MediaCirnoDatabase(object):
    def __init__(self):
        self.conn = sqlite3.connect('db/media-cirnodb.db', timeout=60)
        self.c = self.conn.cursor()
        self.createtables()

    def createtables(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS media(id TEXT, type TEXT, title text, seconds INTEGER, "
                       " PRIMARY KEY(id, type))")

    def insert_media(self, id, title, type, seconds):
        self.c.execute("INSERT OR REPLACE INTO media VALUES(?,?,?, ?)", (id, type, title, seconds))
        self.conn.commit()


class IPCirnoDatabase(object):
    def __init__(self):
        self.conn = sqlite3.connect('db/ip-cirnodb.db', timeout=60)
        self.c = self.conn.cursor()
        self.createtables()

    def createtables(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS ip2user(ipaddr TEXT, name TEXT,"
                       " PRIMARY KEY(ipaddr))")

        self.c.execute("CREATE TABLE IF NOT EXISTS user2ip(name TEXT, ipaddr TEXT,"
                       " PRIMARY KEY(name))")

    def insertuserip(self, ipstr, username):
        if username is None:
            return
        buf=""
        self.c.execute("SELECT name FROM ip2user WHERE ipaddr = ?", [ipstr])
        r = self.c.fetchone()
        if r != None:
            buf=","+str(r[0])
        if username not in buf:
            username=username+buf
            self.c.execute("INSERT OR REPLACE INTO ip2user VALUES (?, ?)",
                           (ipstr, username))
        self.conn.commit()
    def insertuserip2(self, ipstr, username):
        if username is None:
            return
        buf=""
        self.c.execute("SELECT ipaddr FROM user2ip WHERE name = ?", [username])
        r = self.c.fetchone()
        if r != None:
            buf=","+str(r[0])
        if ipstr not in buf:
            ipstr=ipstr+buf
            self.c.execute("INSERT OR REPLACE INTO user2ip VALUES (?, ?)",
                           (username, ipstr))
        self.conn.commit()

    def get_u2ip(self, username):
            self.c.execute("SELECT ipaddr FROM user2ip WHERE name = ?", [username])
            r = self.c.fetchone()
            if r:
                return r[0]
            else:
                return None

class CirnoDatabase(object):
    def __init__(self, name):
        self.conn = sqlite3.connect('db/'+name+'-cirnodb.db', timeout=60)
        self.c = self.conn.cursor()
        self.createtables()
        self.ipdb=IPCirnoDatabase();
        self.mediadb=MediaCirnoDatabase();

    def createtables(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS users(uname TEXT, rank INTEGER,"
                       " PRIMARY KEY(uname))")
        self.c.execute("CREATE TABLE IF NOT EXISTS chat(timestamp INTEGER,"
                       " username TEXT, msg TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS pics(pictures TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS login(time TEXT, login TEXT,"
                       " PRIMARY KEY(time))")
        self.c.execute("CREATE TABLE IF NOT EXISTS ip(uname TEXT, ip TEXT,"
                       " PRIMARY KEY(ip))")
        self.c.execute("CREATE TABLE IF NOT EXISTS ip2(uname TEXT, ip TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS playlist(time TEXT, vid TEXT,"
                       " PRIMARY KEY(time))")
        self.c.execute("CREATE TABLE IF NOT EXISTS chatlog(time TEXT, chat TEXT,"
                       " PRIMARY KEY(time))")
        self.c.execute("CREATE TABLE IF NOT EXISTS mod_new(timestamp INTEGER, time TEXT, mod TEXT,"
                       " PRIMARY KEY(time))")
        self.c.execute("CREATE TABLE IF NOT EXISTS quotes(chatquote TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS version(key TEXT, "
                       "value TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS pl(title TEXT, vid TEXT,"
                       " PRIMARY KEY(vid))")
        self.c.execute("CREATE TABLE IF NOT EXISTS emote_usage(emote TEXT, count INTEGER,"
                       " PRIMARY KEY(emote))")
        self.c.execute("CREATE TABLE IF NOT EXISTS uemote(username TEXT, emote TEXT, count INTEGER,"
                       " PRIMARY KEY(emote))")
        self.c.execute("CREATE TABLE IF NOT EXISTS uwords(username TEXT, word TEXT, count INTEGER,"
                       " PRIMARY KEY(word))")
        self.c.execute("CREATE TABLE IF NOT EXISTS motd(motd TEXT,"
                       " PRIMARY KEY(motd))")
        self.c.execute("CREATE TABLE IF NOT EXISTS css(csshash TEXT, timestamp INTEGER, css TEXT,"
                       " PRIMARY KEY(csshash))")
        self.c.execute("CREATE TABLE IF NOT EXISTS media(id TEXT, title TEXT, type text, seconds INTEGER, "
                       " PRIMARY KEY(id))")
        self.updatetables()

        self.updatetables()

    def updatetables(self):
        if self.getversion() is None:
            self.c.execute("INSERT INTO version(key, value) VALUES (?, ?)",
                           ['dbversion', '1'])
            self.conn.commit()
        elif self.getversion() is '1':
            self.c.execute("ALTER TABLE pics ADD added_by TEXT")
            self.c.execute("UPDATE version SET value = '2' WHERE key = 'dbversion'")
            self.conn.commit()

    def getversion(self):
        self.c.execute("SELECT value FROM version WHERE key = 'dbversion'")
        r = self.c.fetchone()
        if r:
            return r[0]
        else:
            return None

    def insertchat(self, timestamp, username, msg):
        self.c.execute("INSERT INTO chat VALUES(?, ?, ?)",
                       (timestamp, username, msg))
        self.conn.commit()

    def insertuserip(self, username, ip):
        if username is None:
            return


        self.ipdb.insertuserip(ip, username);
        self.ipdb.insertuserip2(ip, username);

        self.c.execute("INSERT OR REPLACE INTO ip VALUES (?, ?)",
                       (username, ip))
        self.c.execute("INSERT OR REPLACE INTO ip2 VALUES (?, ?)",
                       (username, ip))

        self.conn.commit()

    def insertuser(self, username, rank):
        if username is None:
            return

        self.c.execute("INSERT OR REPLACE INTO users VALUES (?, ?)",
                       (username, rank))
        self.conn.commit()

    def insertuserrank(self, username, rank):
        self.c.execute("UPDATE users SET rank = ? WHERE uname = ?",
                       (rank, username))
        self.conn.commit()

    def insertmotd(self,  motd):
        self.c.execute("INSERT OR REPLACE INTO motd VALUES(?)", (motd, ))
        self.conn.commit()

    def insertcss(self, csshash, timestamp, css):
        self.c.execute("INSERT OR REPLACE INTO css VALUES(?, ?, ?)", (csshash, timestamp, css))
        self.conn.commit()


    def getuserrank(self, username):
        self.c.execute("SELECT rank FROM users WHERE uname= ?", [username])
        r = self.c.fetchone()
        if r:
            return list(r)[0]
        else:
            return None

    def getrandom(self, username):
        username = username.split(' ')[0]

        if username:
            self.c.execute("SELECT timestamp, username, msg FROM chat "
                           "WHERE username = ? COLLATE NOCASE "
                           "ORDER BY RANDOM() LIMIT 1", [username])
            r = self.c.fetchone()
            if r:
                return list(r)
            else:
                return None
        else:
            self.c.execute("SELECT timestamp, username, msg FROM "
                           "chat WHERE msg NOT LIKE '/me%' AND "
                           "msg NOT LIKE '$%' ORDER BY RANDOM() LIMIT 1")
            r = self.c.fetchone()
            if r:
                return list(r)
            else:
                return None

    def getquantity(self, username):
        username = username.split(' ')[0]
        self.c.execute("SELECT COUNT(*) AS quantity FROM chat"
                       " WHERE username = ? COLLATE NOCASE LIMIT 1",
                       [username])
        r = self.c.fetchone()
        if r:
            return list(r)[0]
        else:
            return None

    def emotesquantity(self, username):
        username = username.split(' ')[0]
        self.c.execute("SELECT COUNT(*) AS quantity, msg FROM chat"
                       " WHERE username = ? COLLATE NOCASE AND (msg LIKE ':%:' OR msg LIKE '%:  :%:') COLLATE NOCASE LIMIT 1",
                       [username])
        r = self.c.fetchone()
        if r:
            return list(r)[0]
        else:
            return None

    def getpic(self):
        self.c.execute("SELECT pictures FROM pics ORDER BY"
                       " RANDOM() LIMIT 1")
        r = self.c.fetchone()
        if r:
            return list(r)[0]
        else:
            return None

    def getquote(self):
        self.c.execute("SELECT chatquote FROM quotes ORDER BY"
                       " RANDOM() LIMIT 1")
        r = self.c.fetchone()
        if r:
            return list(r)[0]
        else:
            return None
    def insert_pl(self, msg):
        time=msg.split(']', 1)[0][1:]
        m=msg.split(']', 1)[1]
        self.c.execute("INSERT OR REPLACE INTO playlist VALUES(?,?)", (time,m,))
    def insert_chatlog(self, msg):
        time=msg.split(']', 1)[0][1:]
        m=msg.split(']', 1)[1]
        self.c.execute("INSERT OR REPLACE INTO chatlog VALUES(?,?)", (time,m,))
    def insert_playlist(self, vid, title):
        self.c.execute("INSERT OR REPLACE INTO pl VALUES(?,?)", (title,vid))
        self.conn.commit()

    def insert_media(self, id, title, type, seconds):
        self.c.execute("INSERT OR REPLACE INTO media VALUES(?,?,?, ?)", (id, type, title, seconds))
        self.mediadb.insert_media(id, title, type,seconds)
        self.conn.commit()

    def insert_emote(self, emote):
        count=1
        self.c.execute("SELECT count FROM emote_usage WHERE emote= ?", [emote])
        r = self.c.fetchone()
        if r:
            count=list(r)[0]+1
            self.c.execute("UPDATE emote_usage SET count = ? WHERE emote = ?",
                           (count, emote))
            self.conn.commit()
        else:
            self.c.execute("INSERT OR IGNORE INTO emote_usage VALUES(?,?)", (emote,1))
            self.conn.commit()

    def get_emoteusage(self, username):
        if username == None:
            self.c.execute("SELECT emote,count FROM emote_usage ORDER BY"
                           " count DESC LIMIT 7 OFFSET 0")
            r = self.c.fetchall()
            if r:
                return list(r)
            else:
                return None
        else:
            self.c.execute("SELECT emote,count FROM uemote WHERE username = ? ORDER BY"
                           " count DESC LIMIT 7 OFFSET 0", [username])
            r = self.c.fetchall()
            if r:
                return list(r)
            else:
                return None

    def get_wusage(self, username):
        if username == None:
            self.c.execute("SELECT word,count FROM uwords ORDER BY"
                           " count DESC LIMIT 5 OFFSET 0")
            r = self.c.fetchall()
            if r:
                return list(r)
            else:
                return None
        else:
            self.c.execute("SELECT word,count FROM uwords WHERE username = ? ORDER BY"
                           " count DESC LIMIT 5 OFFSET 0", [username])
            r = self.c.fetchall()
            if r:
                return list(r)
            else:
                return None


    def insert_uword(self, username, word):
        count=1
        self.c.execute("SELECT count FROM uwords WHERE word= ? and username= ?", (word, username))
        r = self.c.fetchone()
        if r:
            count=list(r)[0]+1
            self.c.execute("UPDATE uwords SET count=? WHERE word=? and username=?",
                           (count, word, username))
            self.conn.commit()
        else:
            self.c.execute("INSERT OR REPLACE INTO uwords VALUES(?,?,?)", (username,word,1))
            self.conn.commit()

    def insert_uemote(self, username, emote):
        count=1
        self.c.execute("SELECT count FROM uemote WHERE emote= ? and username= ?", (emote, username))
        r = self.c.fetchone()
        if r:
            count=list(r)[0]+1
            self.c.execute("UPDATE uemote SET count=? WHERE emote=? and username=?",
                           (count, emote, username))
            self.conn.commit()
        else:
            self.c.execute("INSERT OR REPLACE INTO uemote VALUES(?,?,?)", (username,emote,1))
            self.conn.commit()

    def insert_login(self, msg):
        time=msg.split(']', 1)[0][1:]
        m=msg.split(']', 1)[1]
        self.c.execute("INSERT OR IGNORE INTO login VALUES(?,?)", (time, m,))
    def insert_mod(self, msg, timestamp):
        time=msg.split(']',1)[0][1:]
        m=msg.split(']',1)[1]
        self.c.execute("INSERT OR IGNORE INTO mod_new VALUES(?,?,?)", (timestamp,time,m,))
    def savepic(self, username, picture):
        self.c.execute("INSERT OR REPLACE INTO pics VALUES(?, ?)", (picture, username))
        self.conn.commit()
