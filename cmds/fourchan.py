import requests
from random import choice
from lib.utils import throttle


class Fourchan(object):

    def fourchanboards(self):
        boardlist = 'https://a.4cdn.org/boards.json'
        try:
            boards = requests.get(boardlist).json()['boards']
            resboards = [board['board'] for board in boards]
        except Exception:
            return
        return resboards

    def get4chanthreads(self, board):
        threadlist = 'https://a.4cdn.org/%s/threads.json' % board
        resboards = self.fourchanboards()
        if board in resboards and resboards:
            threads = requests.get(threadlist).json()
            req = [x['threads'] for x in threads]
            result = [x['no'] for x in sum(req, []) if x]
            return result

    def get4chanpics(self, board):
        threads = self.get4chanthreads(board)
        if threads is None:
            return
        inthread = 'https://a.4cdn.org/%s/thread/{0}.json' % board
        main = 'https://i.4cdn.org/%s/' % board
        posts = requests.get(inthread.format(choice(threads))).json()['posts']
        allowext = {'.jpg', '.png', '.gif'}
        result = ['%s%s%s' % (main, post['tim'], post['ext']) for post in posts
                  if ('filename' in post) and
                  (post.get('ext', None) in allowext)]
        return choice(result) if result else 'Nothing found!'

    @throttle(8)
    def _cmd_4chan(self, cirno, username, args):
        if args not in self.fourchanboards() or args in cirno.disallowed4ch:
            cirno.sendmsg('%s: Board is absent or disabled' % username)
        else:
            randpic = self.get4chanpics(args)
            if randpic:
                cirno.sendmsg('%s: %s' % (username, randpic))


def setup():
    return Fourchan()
