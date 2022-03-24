class Help(object):
    #@throttle(5)
    def _cmd_h(self, cirno, username, args):
                helpmsg="help:!r/!b/!p/!z - rudy/tom/pt/zun,!bj - blackjack,!pick <a b>, !t - trivia, !a - trivia ans,!u - urban, !sw - wordscramb,!uw - wordscramb ans,!sc - wordscramb clue, !d - dict,!rq - riddle,!ra - riddle ans, !spam <usr>,!nspam <usr> - undo spam, !ff  - smutes, !nff - undos ff, !g - giphy, !m - mfc"
                cirno.sendmsg(helpmsg)
    def _cmd_help(self, cirno, username, args):
                helpmsg="help:!r/!b - rudy/tom,!bj - blackjack,!pick <a b>, !t - trivia, !a - trivia ans,!u - urban, !sw - wordscramb,!uw - wordscramb ans,!sc - wordscramb clue, !d - dict,!rq - riddle,!ra - riddle ans, !spam <usr>,!nspam <usr> - undo spam, !ff  - smutes, !nff - undos ff, !g - giphy, !m - mfc"
                cirno.sendmsg(helpmsg)

def setup():
    return Help()
