import requests
import json
import urllib
from lib.utils import throttle
import requests

cookies = {
    '__cfduid': 'd3b5d22278dc1cfcb43abe8ad112f91aa1579611686',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Proxy-Authorization': 'Basic ZmExODg2YTBkZGQ3ZmRjNTIxMjA0NzU2MzY5OGRhNTE6ZmExODg2YTBkZGQ3ZmRjNTIxMjA0NzU2MzY5OGRhNTE=',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers',
}

params = (
    ('method', 'getQuote'),
    ('format', 'json'),
    ('lang', 'en'),
)


qfile=open("db/quoteText.txt", "a+")

class Quotes(object):

    def quotes(self):
        try:
            data = requests.get('https://api.forismatic.com/api/1.0/', headers=headers, params=params, cookies=cookies)
            data = json.loads(str(data.text))
        except Exception:
            return
        return data

    @throttle(5)
    def _cmd_q(self, cirno, username, args):
        result = self.quotes()
        q=result['quoteText']+" - "+ result['quoteAuthor']
        cirno.sendmsg('%s: %s' % (username, q))
        qfile.write(q);
        qfile.write("\n");


def setup():
    return Quotes()
