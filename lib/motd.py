import feedparser
import random

class Feed():
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def link(self):
        return self.link

    def title(self):
        return self.title


class RSSfeeds():
    def __init__(self, url):
        self.url = url
        self.news = []

    def get_feeds(self):
        feeds = feedparser.parse(self.url)
        for entry in feeds.entries:
            if entry.title not in self.news:
                self.news.append(Feed(entry.title, entry.link))

    def shuffle(self):
        random.shuffle(self.news)

    def clear_feeds():
        for i in self.news:
            del i
        self.news = []

class RSS():
    def __init__(self):
        self.rss_feeds = [
            "https://feeds.skynews.com/feeds/rss/world.xml",
            "https://www.vox.com/rss/world/index.xml",
            "https://www.scmp.com/rss/91/feed",
            "https://www.independent.co.uk/news/world/rss",
            "https://www.rt.com/rss/news/",
            "https://www.globalissues.org/news/feed",
            "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml",
            "https://www.france24.com/en/rss",
            "https://www.aljazeera.com/xml/rss/all.xml",
            "https://www.newsrust.com/feeds/posts/default?alt=rss",
            "https://feeds.thelocal.com/rss/es",
            "https://247newsaroundtheworld.com/feed/",
            "https://www.dailytelegraph.com.au/news/world/rss",
            "https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=6311"
            "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
            "https://www.worldpress.org/feeds/topstories.xml",
            "https://www.ft.com/global-economy?format=rss",
            "https://www.sciencedaily.com/rss/all.xml",
            "https://moxie.foxnews.com/feedburner/world.xml",
            "https://globalnews.ca/world/feed/",
            "https://www.thehindu.com/news/international/feeder/default.rss",
            "https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf"
            #"https://feeds.24.com/articles/news24/World/rss"
        ]
        self.rssobjs=[]
        self.rss_load()
        self.news = []

    def rss_load(self):
        for url in self.rss_feeds:
            self.rssobjs.append(RSSfeeds(url))

    def rss_fetch(self):
        for rss in self.rssobjs:
            rss.get_feeds()
            random.seed()
            rss.shuffle()

    def rss_populate(self):
        self.news = []
        for rss in self.rssobjs:
            j = 0
            random.shuffle(rss.news)
            for i in rss.news:
                il = i.title.lower()
                if "latest videos" in il:
                    continue
                if "latest news" in il:
                    continue
                self.news.append(i)
                j = j + 1
                if j == 1:
                    break
            random.shuffle(self.news)

class MOTD():
    def __init__(self):
        self.motd_start="<center> <marquee>"
        self.font="<font color=\"#00FF00\" size=\"4\">"
        self.breakgif="<img src=\"https://c.tenor.com/zQAPAoVVe5kAAAAM/damn-breaking-news.gif\" height=\"50\" />"
        self.fontend="</font>"
        self.motd_end="</marquee> </center>"
        self.robj=RSS()

    def get_updated_news(self):
        self.robj.rss_fetch()

    def get_motd(self):
        self.robj.rss_populate()
        motd = self.motd_start + self.font
        for i in self.robj.news:
            motd += self.breakgif + "<a target=\"_blank\" rel=\"noopener noreferrer\" href=\""
            motd +=i.link+"\">"+i.title+"</a>"
        motd += self.fontend + self.motd_end
        return motd
