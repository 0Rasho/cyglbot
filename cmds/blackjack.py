import os
import random
from random import choice, randint, uniform
import giphypop
import requests

#decks = input("Enter number of decks to use: ")
decks = 1
# user chooses number of decks of cards to use
#deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*(int(decks)*4)
deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS']

cards={}
#cards[2]="https://i.postimg.cc/fR2z9n3P/c2.png"
#cards[3]="https://i.postimg.cc/SKHmg6f7/c3.png"
#cards[4]="https://i.postimg.cc/1z890Cw3/c4.png"
#cards[5]="https://i.postimg.cc/bJbpWZ6X/c5.png"
#cards[6]="https://i.postimg.cc/kGv9Mk3f/c6.png"
#cards[7]="https://i.postimg.cc/15MPkhKz/c7.png"
#cards[8]="https://i.postimg.cc/59BfmFYL/c8.png"
#cards[9]="https://i.postimg.cc/c4d0k4wj/c9.png"
#cards[10]="https://i.postimg.cc/PJjTjdcC/c10.png"
#cards['J']="https://i.postimg.cc/K8zFFq9D/cj.png"
#cards['Q']="https://i.postimg.cc/BvP0P8f8/cq.png"
#cards['K']="https://i.postimg.cc/zGcNfC6Z/ck.png"
#cards['A']="https://i.postimg.cc/Jh7WKTXk/ca.png"

cards['2C']="https://i.postimg.cc/KzS8ZGHr/2C.png"
cards['2D']="https://i.postimg.cc/D07fXCFS/2D.png"
cards['2H']="https://i.postimg.cc/ZR8K0kkk/2H.png"
cards['2S']="https://i.postimg.cc/sxKj9pDw/2S.png"
cards['3C']="https://i.postimg.cc/MZYpS8bV/3C.png"
cards['3D']="https://i.postimg.cc/fRVzmS4f/3D.png"
cards['3H']="https://i.postimg.cc/tCCCRm2f/3H.png"
cards['3S']="https://i.postimg.cc/gkScxq70/3S.png"
cards['4C']="https://i.postimg.cc/9QsWpXC5/4C.png"
cards['4D']="https://i.postimg.cc/C1sSSjDS/4D.png"
cards['4H']="https://i.postimg.cc/VNMzHykS/4H.png"
cards['4S']="https://i.postimg.cc/bJhp76Zm/4S.png"
cards['5C']="https://i.postimg.cc/mkZRDtNM/5C.png"
cards['5D']="https://i.postimg.cc/wTGHqxty/5D.png"
cards['5H']="https://i.postimg.cc/Vs4mhWmF/5H.png"
cards['5S']="https://i.postimg.cc/VNy8t7Wz/5S.png"
cards['6C']="https://i.postimg.cc/BnP3XWDh/6C.png"
cards['6D']="https://i.postimg.cc/Gh2dnTpn/6D.png"
cards['6H']="https://i.postimg.cc/6QdNfdMn/6H.png"
cards['6S']="https://i.postimg.cc/rmM2nKHb/6S.png"
cards['7C']="https://i.postimg.cc/MT52hz2G/7C.png"
cards['7D']="https://i.postimg.cc/5ytdJDbS/7D.png"
cards['7H']="https://i.postimg.cc/C56yxJKT/7H.png"
cards['7S']="https://i.postimg.cc/2jHNGj7c/7S.png"
cards['8C']="https://i.postimg.cc/8P9Q8y3L/8C.png"
cards['8D']="https://i.postimg.cc/g0bCjxGJ/8D.png"
cards['8H']="https://i.postimg.cc/T3b8TVMF/8H.png"
cards['8S']="https://i.postimg.cc/TYpM48kR/8S.png"
cards['9C']="https://i.postimg.cc/bv0KtqvR/9C.png"
cards['9D']="https://i.postimg.cc/TwRBjBLv/9D.png"
cards['9H']="https://i.postimg.cc/SsD3gVC2/9H.png"
cards['9S']="https://i.postimg.cc/SNw51n2r/9S.png"
cards['JC']="https://i.postimg.cc/65GbZBjG/JC.png"
cards['JD']="https://i.postimg.cc/Bn9YcRk7/JD.png"
cards['JH']="https://i.postimg.cc/qqNbjrpS/JH.png"
cards['JS']="https://i.postimg.cc/y6GrWDPH/JS.png"
cards['QC']="https://i.postimg.cc/xCCt1QN8/QC.png"
cards['QD']="https://i.postimg.cc/QtySBzcb/QD.png"
cards['QH']="https://i.postimg.cc/2yLGnxwf/QH.png"
cards['QS']="https://i.postimg.cc/s1FcmZ6G/QS.png"
cards['KC']="https://i.postimg.cc/Wzx9yy33/KC.png"
cards['KD']="https://i.postimg.cc/P5W662kX/KD.png"
cards['KH']="https://i.postimg.cc/fbM81mwx/KH.png"
cards['KS']="https://i.postimg.cc/LsvxS5XG/KS.png"
cards['AC']="https://i.postimg.cc/2ytJD6HC/AC.png"
cards['AD']="https://i.postimg.cc/cJcbJTD9/AD.png"
cards['AH']="https://i.postimg.cc/Qt4YQCZc/AH.png"
cards['AS']="https://i.postimg.cc/sXD0GSqV/AS.png"
cards['10C']="https://i.postimg.cc/jSP1pRyr/10C.png"
cards['10D']="https://i.postimg.cc/NFFVSTkN/10D.png"
cards['10H']="https://i.postimg.cc/QxBwqQtC/10H.png"
cards['10S']="https://i.postimg.cc/J7YSJ6RS/10S.png"



# initialize scores
wins = 0
losses = 0
bj_in_progress=0
g = giphypop.Giphy()
#gif_list=g.search_list("topless girls", limit=400)
#lgif_list=g.search_list("loser", limit=200)

offset=0
gif_list=[]

def get_gif_list(last_offset):
    file1 = open('db/cache', 'r')
    file1.seek(0, os.SEEK_SET)
    for quote in file1:
        quote=quote.strip('\n')
        quote=quote.strip()
        gif_list.append(quote)
    file1.close()
    #print gif_list

#    params = {'q': ("sexy girls")}
#    params['api_key'] = "dc6zaTOxFJmzC"
#    params['limit'] = 25
#    params['offset'] = last_offset
#    resp = requests.get("http://api.giphy.com/v1/gifs/search", params=params)
#    k=(resp.json())
#    k= k['data']
#    i=0
#    while i < len(k):
#        url=str(k[i]['images']['fixed_width']['url'])+".pic"
#        gif_list.append(url)
#        i=i+1

#get_gif_list(0)
#print gif_list
#print len(gif_list)
#get_gif_list(25)
#print gif_list
#print len(gif_list)
#print gif_list.pop(0)

class BlackJACK(object):
    def deal(self, deck):
        hand = []
        for i in range(2):
            random.shuffle(deck)
            card = deck.pop()
            #if card == 11:card = "J"
            #if card == 12:card = "Q"
            #if card == 13:card = "K"
            #if card == 14:card = "A"
            hand.append(card)
        return hand

    def total(self, hand):
        total = 0
        for card in hand:
            card=card[:-1]
            #print "total", card
            if card == "J" or card == "Q" or card == "K":
                total+= 10
            elif card == "A":
                if total >= 11: total+= 1
                else: total+= 11
                #total+= 1
            else: total += int(card)
        return total

    def hit(self, hand):
        card = deck.pop()
        #if card == 11:card = "J"
        #if card == 12:card = "Q"
        #if card == 13:card = "K"
        #if card == 14:card = "A"
        hand.append(card)
        return hand

    def blackjack(self, cirno, username, dealer_hand, player_hand):
        global bj_in_progress

        dbuf=""
        for k in dealer_hand:
            dbuf+=":"+str(k)+" "
        pbuf=""
        for k in player_hand:
            pbuf+=":"+str(k)+" "

        if self.total(player_hand) == 21:
            cirno.sendmsg (username+" got a Blackjack! "+pbuf)
            self.send_gif(cirno, username, "boobs")
            bj_in_progress=0
        elif self.total(dealer_hand) == 21:
            cirno.sendmsg ("Dealer got a blackjack. "+dbuf)
            self.send_gif(cirno, username, "loser")
            bj_in_progress=0

    def send_gif(self, cirno, username, search_str):
        if search_str == "boobs":
            #print "sending gif"
            try:
                k = gif_list.pop(randint(0, len(gif_list)))
            except:
                get_gif_list(offset)
                #print "get"
                k = gif_list.pop(randint(0, len(gif_list)))
                #print "--k", k
            if k:
                cirno.sendmsg('%s: %s' % (username, k))
                return
        else:
            k=lgif_list.pop(randint(0, len(lgif_list)))
            if k:
                url=str(k['fixed_width']['url'])+".pic"
                cirno.sendmsg('%s: %s' % (username, url))
                return

        results = g.search_list(search_str, limit=randint(75,250))
        length=len(results)
        if length == 0:
                results = g.search_list(search_list, limit=randint(50,75))
                length=len(results)
        if length == 0:
                results = g.search_list(search_list, limit=randint(25,50))
                length=len(results)
        if length == 0:
                results = g.search_list(search_list, limit=randint(1,25))
                length=len(results)
        if length == 0:
                results = g.search_list(search_list, limit=randint(0,1))
                length=len(results)
        if length > 0:
            rand = randint(0, length-1)
            url=str(results[rand]['fixed_width']['url'])+".pic"
            cirno.sendmsg('%s: %s' % (username, url))

    def score(self, cirno, username, dealer_hand, player_hand):
            global bj_in_progress
            dbuf=""
            for k in dealer_hand:
                dbuf+=":"+str(k)+" "

            pbuf=""
            for k in player_hand:
                pbuf+=":"+str(k)+" "

            ptotal = self.total(player_hand)
            dtotal = self.total(dealer_hand)
            cirno.sendmsg("Dealer : "+dbuf+" = "+str(dtotal))
            cirno.sendmsg(username+" : "+pbuf+ " = "+str(ptotal))

            if self.total(player_hand) == 21:
                cirno.sendmsg (username+" got a Blackjack!")
                self.send_gif(cirno, username, "boobs")
            elif self.total(dealer_hand) == 21:
                cirno.sendmsg ("Dealer got a blackjack.")
                self.send_gif(cirno, username, "loser")
            elif self.total(player_hand) > 21:
                cirno.sendmsg (username+" => You busted.")
                self.send_gif(cirno, username, "loser")
            elif self.total(dealer_hand) > 21:
                cirno.sendmsg ("Dealer busts. "+username+" win!")
                self.send_gif(cirno, username, "boobs")
            elif self.total(player_hand) < self.total(dealer_hand):
                cirno.sendmsg (username+" score isn't higher than the Dealer. "+ username+" lost.")
                self.send_gif(cirno, username, "loser")
            elif self.total(player_hand) > self.total(dealer_hand):
                cirno.sendmsg (username+" score is higher than the Dealer "+username+" win")
                self.send_gif(cirno, username, "boobs")
            elif self.total(player_hand) == self.total(dealer_hand):
                cirno.sendmsg (username+" => Dealer is in love with you")
            #bj_in_progress=0

    def _cmd_bj(self, cirno, username, args):
        global deck
        global bj_in_progress
        global player_hand
        global dealer_hand
        if not args:
            bj_in_progress=1
            deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS']
            random.shuffle(deck)
            random.shuffle(deck)
            random.shuffle(deck)
            random.shuffle(deck)
            random.shuffle(deck)
            random.shuffle(deck)
            random.shuffle(deck)
            random.shuffle(deck)
            random.shuffle(deck)
            dealer_hand = self.deal(deck)
            player_hand = self.deal(deck)
            cirno.sendmsg ("Dealer :  :" + str(dealer_hand[0]))
            buf=""
            for k in player_hand:
                buf+=":"+str(k)+" "
            cirno.sendmsg (username+" : " + buf + " total of " + str(self.total(player_hand)))
            self.blackjack(cirno, username, dealer_hand, player_hand)
            if bj_in_progress == 1:
                cirno.sendmsg(username+": Hit '!bj h' or Stand '!bj s'?")
        else:
            if bj_in_progress == 0:
                return
            choice=list(args)[0]
            if choice == 'h':
                self.hit(player_hand)
                buf=""
                for k in player_hand:
                    buf+=":"+str(k)+" "

                ptotal=self.total(player_hand)
                cirno.sendmsg(username+" : "+buf+" = "+str(ptotal))
                #cirno.sendmsg(username+" : "+buf)
                if self.total(player_hand)>21:
                    dbuf=""
                    for k in dealer_hand:
                        dbuf+=":"+str(k)+" "

                    #pbuf=""
                    #for k in player_hand:
                    #    pbuf+=cards[k]+" "

                    dtotal=self.total(dealer_hand)
                    cirno.sendmsg("Dealer : "+dbuf+" = "+str(dtotal))
                    #cirno.sendmsg(username+" : "+pbuf)
                    cirno.sendmsg(username+' busted')
                    self.send_gif(cirno, username, "loser")
                    bj_in_progress=0
                else:
                    cirno.sendmsg(username+" => Hit '!bj h' or Stand '!bj s'?")
            elif choice == 's':
                while self.total(dealer_hand)<17:
                    self.hit(dealer_hand)
                    buf=""
                    for k in dealer_hand:
                        buf+=":"+str(k)+" "
                    dtotal=self.total(dealer_hand)
                    cirno.sendmsg("Dealer : "+buf+" = "+str(dtotal))
                    if self.total(dealer_hand)>21:
                        #dbuf=""
                        #for k in dealer_hand:
                        #    dbuf+=cards[k]+" "

                        pbuf=""
                        for k in player_hand:
                            pbuf+=":"+str(k)+" "
                        #cirno.sendmsg("Dealer : "+dbuf)
                        ptotal=self.total(player_hand)
                        cirno.sendmsg(username+" : "+pbuf+" = "+str(ptotal))
                        cirno.sendmsg("Dealer busts, "+username+" wins!")
                        self.send_gif(cirno, username, "boobs")
                        bj_in_progress=0
                        return
                self.score(cirno, username, dealer_hand,player_hand)
                
def setup():
    random.seed()
    return BlackJACK()
