import sqlite3 as lite

conn = lite.connect('db/101-cirnodb.db')
cur = conn.cursor()
'''
cur.execute("DELETE FROM chat")
cur.execute("DELETE FROM mod")
cur.execute("DELETE FROM login")
cur.execute("DELETE FROM playlist")
'''
#cur.execute('SELECT name from sqlite_master where type= "table"')
#print(cur.fetchall())
#a='[Wed Oct 09 2019 13:37:33] [login] Accepted connection from Tor exit at BFE.fDb.Cmy.sAl\naaa'.split('\n')
#print a
#msg=a[0]
#print msg
#cur.execute("INSERT INTO login VALUES(?)", (msg,))
#cur.execute("SELECT * FROM login")
#print(cur.fetchall())
conn.commit()

def get_posts():
    lmsg=""
    cur.execute("SELECT * FROM chat")
    r= cur.fetchall()
    for i in r:
        try:
                    name=i[1]
                    msg=i[2].encode('ascii','ignore')
                    #if name == "Melipal":
                        #print("\033[34m\033[01m %12s\033[0m : \033[32m%s\033[0m" % (i[1], i[2].encode('ascii','ignore')))
                    print("%s : %s" % (i[1], i[2].encode('ascii','ignore')))
                    #print msg
                    lmsg=msg
        except:
                pass

def get_login():
    lmsg=""
    cur.execute("SELECT * FROM login")
    r= cur.fetchall()
    for i in r:
        try:
            print(i[0], i[1])
        except:
                pass
def get_mod():
    lmsg=""
    cur.execute("SELECT * FROM mod_new")
    r= cur.fetchall()
    for i in r:
        try:
            print(i[1], i[2])
        except:
                pass

def get_pl():
    lmsg=""
    cur.execute("SELECT * FROM playlist")
    r= cur.fetchall()
    for i in r:
        try:
            print(i[0], i[1])
        except:
                pass

def get_ip():
    lmsg=""
    cur.execute("SELECT * FROM ip2")
    r= cur.fetchall()
    for i in r:
        try:
            print(i[1], i[0])
        except:
                pass
def get_usrs():
    lmsg=""
    cur.execute("SELECT * FROM users")
    r= cur.fetchall()
    for i in r:
        try:
            print(i[0], i[1])
        except:
                pass
def get_chatlog():
    lmsg=""
    cur.execute("SELECT * FROM chatlog")
    r= cur.fetchall()
    for i in r:
        try:
            print(i[0], i[1])
        except:
                pass
def insert_uword(username, word):
    count=1
    cur.execute("SELECT count FROM uwords WHERE word= ? and username= ?", (word, username))
    r = cur.fetchone()
    if r:
        count=list(r)[0]+1
        cur.execute("UPDATE uwords SET count=? WHERE word=? and username=?",
                       (count, word, username))
    else:
        cur.execute("INSERT OR IGNORE INTO uwords VALUES(?,?,?)", (username,word,1))

def insert_uemote(username, emote):
    count=1
    cur.execute("SELECT count FROM uemote WHERE emote= ? and username= ?", (emote, username))
    r = cur.fetchone()
    if r:
        count=list(r)[0]+1
        cur.execute("UPDATE uemote SET count=? WHERE emote=? and username=?",
                       (count, emote, username))
    else:
        cur.execute("INSERT OR IGNORE INTO uemote VALUES(?,?,?)", (username,emote,1))

def insert_emote(emote):
        count=1
        cur.execute("SELECT count FROM emote_usage WHERE emote= ?", [emote])
        r = cur.fetchone()
        if r:
            count=list(r)[0]+1
            cur.execute("UPDATE emote_usage SET count = ? WHERE emote = ?",
                           (count, emote))
        else:
            cur.execute("INSERT OR IGNORE INTO emote_usage VALUES(?,?)", (emote,1))


def update_text_db():
    f=open("chaa1", "r")
    L=f.readlines()
    for i in L:
        i=i.strip()
        if "href=\"https" in i:
            continue
        emotes=i.split(" : ")
        username=emotes[0]
        try:
            emotes=emotes[1].split()
        except:
            continue
        for e_m in emotes:
            if e_m.startswith(":") or e_m.startswith("\\") or e_m.startswith("/"):
                if e_m != "/></a>":
                    insert_emote(e_m)
                    insert_uemote(username, e_m)
            else:
                if len(e_m) > 3:
                    insert_uword(username, e_m)
    conn.commit()

#update_text_db()
#conn.commit()
#get_ip()
#get_usrs()
#cur.execute('SELECT name from sqlite_master where type= "table"')
#print(cur.fetchall())
#get_posts()
#get_chatlog()
get_pl()
#get_mod()
#get_login()
