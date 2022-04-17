import os
import random
from random import choice, randint, uniform

class Dump():
    def sendmsg(self, buf):
        print(buf)

class BJPlayer():
    def __init__(self, name):
        self.name = name
        self.is_player_out = False
        self.hand = []
        self.bet = 0
    
class BlackJACK2():
    def __init__(self, players):
        self.players=[]
        for i in players:
            self.players.append(BJPlayer(i))
        self.deck = self.get_deck()
        self.dealer_hand = []
        self.next_player = self.players[0].name
        self.is_deal_done = False

    def deal(self):
        card = self.deck.pop()
        return card

    def total(self, hand):
        total = 0
        for card in hand:
            card=card[:-1]
            if card == "J" or card == "Q" or card == "K":
                total+= 10
            elif card == "A":
                if total >= 11: total+= 1
                else: total+= 11
                #total+= 1
            else: total += int(card)
        return total

    def hit(self, hand):
        card = self.deck.pop()
        hand.append(card)
        return hand

    def deal_blackjack(self, cirno, plyr):
        player_hand = plyr.hand
        pbuf=""
        for k in player_hand:
            pbuf+=":"+str(k)+" "
        if self.total(player_hand) == 21:
            cirno.sendmsg (plyr.name+" got a Blackjack! "+pbuf)
            plyr.is_player_out = True

    def score(self, cirno):
            dbuf=""
            for k in self.dealer_hand:
                dbuf+=":"+str(k)+" "

            dtotal = self.total(self.dealer_hand)
            cirno.sendmsg("Dealer : "+dbuf+" = "+str(dtotal))
            pbuf=""
            for plyr in self.players: 
                username = plyr.name
                player_hand = plyr.hand
                for k in player_hand:
                    pbuf+=":"+str(k)+" "
                ptotal = self.total(player_hand)
                cirno.sendmsg(username+" : "+pbuf+ " = "+str(ptotal))

                if self.total(player_hand) == 21:
                    cirno.sendmsg (username+" got a Blackjack!")
                elif self.total(self.dealer_hand) == 21:
                    cirno.sendmsg ("Dealer got a blackjack.")
                elif self.total(player_hand) > 21:
                    cirno.sendmsg (username+" => You busted.")
                elif self.total(self.dealer_hand) > 21:
                    cirno.sendmsg ("Dealer busts. "+username+" win!")
                elif self.total(player_hand) < self.total(self.dealer_hand):
                    cirno.sendmsg (username+" score isn't higher than the Dealer. "+ username+" lost.")
                elif self.total(player_hand) > self.total(self.dealer_hand):
                    cirno.sendmsg (username+" score is higher than the Dealer "+username+" win")
                elif self.total(player_hand) == self.total(self.dealer_hand):
                    cirno.sendmsg (username+" => Dealer is in love with you")
            #undo bprogress
                self.bj_in_progress=0

    def get_deck(self):
        random.seed()
        random.seed()
        deck = ['2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AC', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD', 'AD', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AH', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AS']*(randint(6,8))
        random.seed()
        random.shuffle(deck)
        random.shuffle(deck)
        random.seed()
        random.shuffle(deck)
        random.shuffle(deck)
        random.seed()
        random.shuffle(deck)
        random.seed()
        random.shuffle(deck)
        random.shuffle(deck)
        random.seed()
        random.shuffle(deck)
        random.seed()
        random.shuffle(deck)
        random.seed()
        random.seed()
        cut = randint(1,2)
        dlen = (len(deck))/2
        if cut == 1:
            return deck[:len(deck)//2]
        elif cut == 2:
            return deck[len(deck)//2:]
        else:
            print("error deck cut")
        return deck

    def getnextplayer(self, cplayer):
        i=0
        if self.is_deal_done == True:
            while i < len(self.players):
                plyr = self.players[i]
                if plyr.name == cplayer:
                    i = i + 1
                    break
                i = i + 1
        while i < len(self.players):
            plyr = self.players[i]
            if plyr.is_player_out == False:
                self.next_player = plyr.name
                return
            i = i + 1

        self.next_player = None
        self.bj_in_progress = 0

    def getplayer(self, cplayer):
        i=0
        for plyr in self.players:
            if plyr.name == cplayer:
                return plyr
        return None

    def deal_cards(self, cirno, username):
        self.bj_in_progress = 1;
        for i in range(2):
            for plyr in self.players:
                plyr.hand.append(self.deal())
            self.dealer_hand.append(self.deal())

        cirno.sendmsg ("Dealer :  :" + str(self.dealer_hand[0]))
        for plyr in self.players:
            player_hand = plyr.hand
            buf=""
            for k in player_hand:
                buf+=":"+str(k)+" "
            cirno.sendmsg (plyr.name+" : " + buf + " : " + str(self.total(player_hand)))
        
        for plyr in self.players:
            self.deal_blackjack(cirno, plyr)

        self.getnextplayer(self.next_player)

        self.is_deal_done = True

        if self.bj_in_progress == 1:
            cirno.sendmsg(self.next_player+": Hit '!bj h' or Stand '!bj s'?")

    def player_hit(self, cirno, username):
        plyr = self.getplayer(username)
        if plyr == None:
            print("invalid username")
            return
        player_hand = plyr.hand
        self.hit(player_hand)
        buf=""
        print(username, player_hand)
        for k in player_hand:
            buf+=":"+str(k)+" "

        ptotal=self.total(player_hand)
        cirno.sendmsg(username+" : "+buf+" = "+str(ptotal))
        if self.total(player_hand) == 21:
            self.deal_blackjack(cirno, plyr)
            self.getnextplayer(username)
            if self.bj_in_progress == 1:
                cirno.sendmsg(self.next_player+" => Hit '!bj h' or Stand '!bj s'?")
        elif self.total(player_hand) > 21:
            cirno.sendmsg(username+' busted')
            plyr.is_player_out = True
            self.getnextplayer(username)
            if self.next_player:
                cirno.sendmsg(self.next_player+" => Hit '!bj h' or Stand '!bj s'?")
            else:
                self.bj_in_progress=0
        else:
            cirno.sendmsg(username+" => Hit '!bj h' or Stand '!bj s'?")

    def player_stand(self, cirno, username):
         plyr = self.getplayer(username)
         if plyr == None:
             print("invalid username")
             return
         print(self.next_player, username)
         self.getnextplayer(username)
         print(self.next_player, username)
         if self.next_player and self.next_player != username:
             cirno.sendmsg(self.next_player+": Hit '!bj h' or Stand '!bj s'?")
             return
         while self.total(self.dealer_hand) < 17:
             self.hit(self.dealer_hand)
             buf=""
             for k in self.dealer_hand:
                 buf+=":"+str(k)+" "
             dtotal=self.total(self.dealer_hand)
             cirno.sendmsg("Dealer : "+buf+" = "+str(dtotal))
             if self.total(self.dealer_hand) > 21:
                 cirno.sendmsg("Dealer busts!")
                 for plyr in self.players:
                     pbuf=""
                     player_hand = plyr.hand
                     for k in player_hand:
                         pbuf+=":"+str(k)+" "
                     ptotal=self.total(player_hand)
                     cirno.sendmsg(plyr+" : "+pbuf+" = "+str(ptotal))
                     cirno.sendmsg(plyr+" wins!")
                 self.bj_in_progress=0
                 return
         self.score(cirno)

    def playgame(self, cirno, username, choice):
        if self.bj_in_progress == 0:
            print("bj not in progress")
            return
        if self.next_player != username:
            cirno.sendmsg(username+" - :nono not your turn")
            return
        if choice == 'h':
            self.player_hit(cirno, username)
        elif choice == 's':
            self.player_stand(cirno, username)
        if self.bj_in_progress == 0:
            cirno.bjplayers = []
            cirno.is_bj_running = False
                
class BJ(object):
    def _cmd_bet(self, cirno, username, args):
        if cirno.is_bj_running:
            return
        if username not in cirno.bjplayers:
            cirno.bjplayers.append(username)
    def _cmd_bj(self, cirno, username, args):
        if len(cirno.bjplayers) == 0:
            cirno.sendmsg("Place your bets!: !bet and !bj to start game")
        else:
            cirno.is_bj_running = True
            if not args:
                cirno.bjgame = BlackJACK2(cirno.bjplayers)
                cirno.bjgame.deal_cards(cirno, username)
            else:
                choice=list(args)[0]
                cirno.bjgame.playgame(cirno, username, choice)
                
def setup():
    random.seed()
    return BJ()
