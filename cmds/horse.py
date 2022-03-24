import urllib
import requests
from bs4 import BeautifulSoup
import time


records = {} # storeo all of the records in this list

class HorseRace(object):
    def _cmd_hu(self, cirno, username, args):
        records.clear()
        if not args:
            url="https://www.letrot.com/stats/fiche-course/2019-11-17/7500/4/partants/tableau"
        soup = BeautifulSoup(args, "html.parser")
        vidlist=[a['href'] for a in soup.find_all('a')]
        url=vidlist[0]
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        tabulka = soup.find("table", {"class" : "table-datas fixed_result_table"})
        n=0
        for row in tabulka.findAll('tr'):
            done=0
            k=0
            col = row.findAll('td')
            for i in col:
                if len(i.text):
                    '''
                    if done == 0:
                        for m in i.find_all('a', href=True):
                            print "Found the URL:", m['href']
                            done=1
                            r1 = requests.get(m['href'])
                            soup1 = BeautifulSoup(r1.text)
                            print soup1
                            tabulka1 = soup1.find("table", {"class" : "table-datas dataTable no-footer"})
                            print tabulka1
                            n1=0
                            for row1 in tabulka1.findAll('tr'):
                                done1=0
                                k1=0
                                col1 = row1.findAll('td')
                                for i1 in col1:
                                    print i1.text

                    '''
                    try:
                        records[n][k]=i.text
                    except:
                        records[n]={}
                        records[n][k]=i.text
                        pass
                    k=k+1
            n=n+1
    def _cmd_hr(self, cirno, username, args):
         for i in records:
            if args.lower() in records[i][1].lower():
                idx=len(records[i]) - 4
                cirno.sendmsg("%s => %s" % (args, str(records[i][idx])))
                return

    def _cmd_hl(self, cirno, username, args):
         buf=""
         for i in records:
            buf+=records[i][1].lower()+","
         cirno.sendmsg("%s => %s" % (args, buf))

    def _cmd_ha(self, cirno, username, args):
        k=0
        for i in records:
            if args.lower() in records[i][1].lower():
                idx=len(records[i]) - 4
                a=records[i][idx].split(' ')
                avg=0
                for i in a:
                    if '(' in i:
                        continue
                    if i  == 'Da':
                        k+=1
                        avg += 5
                        continue
                    avg+=int(i[0])
                    k+=1
                cirno.sendmsg("%s => %d" % (args, avg/k))
                return

    def _cmd_hal(self, cirno, username, args):
        for i in records:
                k=0
                name=records[i][1].lower()
                idx=len(records[i]) - 4
                a=records[i][idx].split(' ')
                avg=0
                for i in a:
                    if '(' in i:
                        avg+=5
                        k+=1
                        continue
                    if i  == 'Da':
                        k+=1
                        avg += 5
                        continue
                    try:
                        avg+=int(i[0])
                        k+=1
                    except:
                        continue
                cirno.sendmsg("%s => %d %d" % (name, avg/k, k))
                time.sleep(0.5)

    def _cmd_hp(self, cirno, username, args):
        results={}
        pp=0
        for i in records:
                top3_winner=0
                recent3_results=0
                k=0
                name=records[i][1].lower()
                idx=len(records[i]) - 4
                a=records[i][idx].split(' ')
                avg=0
                done=0
                for i in a:
                    if done < 3:
                        try:
                            r=int(i[0])
                            if r == 0:
                                r=10
                            recent3_results+=r
                            done+=1
                        except:
                            recent3_results+=10
                            done+=1
                            pass
                    if '(' in i:
                        avg+=5
                        k+=1
                        continue
                    if i  == 'Da':
                        k+=1
                        avg += 5
                        continue
                    try:
                        r=int(i[0])
                        if r == 0:
                            r=5
                        if r < 3:
                            top3_winner+=1
                        avg+=r
                        k+=1
                    except:
                        avg+=10
                        k+=1
                        continue
                perc=top3_winner*100/k
                if perc <= 25:
                    avg+=100
                elif perc <= 50:
                    avg+=50
                elif perc <= 75:
                    avg+=25
                elif perc <= 90:
                    avg+=5
                elif perc <= 100:
                    avg+=0
                ppp=0
                precr = (recent3_results)/3
                if precr <= 3:
                    avg-=10
                results[pp]=[]
                results[pp].append(avg/k)
                results[pp].append(precr)
                results[pp].append(name)
                pp+=1
        s=sorted(results.items(), key=lambda e: e[1][0])
        buf=""
        k=0
        for i in s:
            buf+=i[1][2].upper()
            k+=1
            if k == 7:
                buf+=" "
                break
            else:
                buf+=", "
        cirno.sendmsg("Probable winners: %s" % (buf))

def setup():
    return HorseRace()
