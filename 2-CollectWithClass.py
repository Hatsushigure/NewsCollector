import re
import textwrap
from nntplib import NNTP
from urllib.request import urlopen


class NewsItem:
    def __init__(self, title, body):
        self.title = title
        self.body = body

class NewsAgent:
    def __init__(self):
        self.sources = []
        self.destinations = []

    def addSource(self, source):
        self.sources.append(source)

    def addDestination(self, destination):
        self.destinations.append(destination)

    def distributeNews(self):
        items = []
        for source in self.sources:
            items.extend(source.getItems())
        for destination in self.destinations:
            destination.receive(items)

class NntpSource:
    def __init__(self, host, group):
        self.host = host
        self.group = group
        self.maxCount = 0

    def setMaxCount(self, count):
        self.maxCount = count

    def getItems(self):
        server = NNTP(self.host)
        resp, count, first, last, name = server.group(self.group)
        resp, overviews = server.over((last - self.maxCount + 1, last))
        for newsId, overview in overviews:
            title = overview["subject"]
            resp, info = server.body(newsId)
            body = '\n'.join(line.decode("latin") for line in info.lines) + "\n\n"
            yield NewsItem(title, body)
        server.quit()

class SimpleHtmlSource:
    def __init__(self, url, titlePattern, bodyPattern, encoding="utf8"):
        self.url = url
        self.titlePattern = re.compile(titlePattern)
        self.bodyPattern = re.compile(bodyPattern)
        self.encoding = encoding

    def getItems(self):
        text = urlopen(self.url).read().decode(self.encoding)
        titles = self.titlePattern.findall(text)
        bodies = self.bodyPattern.findall(text)
        for title, body in zip(titles, bodies):
            yield NewsItem(title, textwrap.fill(body) + '\n')

class PlainTextDestination:
    def receive(self, items):
        for item in items:
            print(item.title)
            print(item.body)

class HtmlDestination:
    def __init__(self, filename):
        self.filename = filename

    def receive(self, items):
        out = open(self.filename, 'w', encoding="utf8")
        print("""<html>
    <head>
        <title>Today's News</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>Today's News</h1>""", file=out)
        print(' ' * 8 + "<ul>", file=out)
        id = 0
        for item in items:
            id += 1
            print(' ' * 12 + '<li><a href="#{}">{}</a></li>'
              .format(id, item.title), file=out)
        print(' ' * 8 + "</ul>", file=out)
        id = 0
        for item in items:
            id += 1
            print(' ' * 8 + '<h2><a id="{}">{}</a></h2>'
              .format(id, item.title), file=out)
            print(' ' * 8 + '<pre>{}        </pre>'.format(item.body), file=out)
        print("""    </body>
</html>
        """, file=out)

agent = NewsAgent()
bbcUrl = 'https://bbc.com'
bbcTitle = r'<h2.*?>(.*?)<'
bbcBody = r'</h2></div></div><p.*?>(.*?)</p>'
bbc = SimpleHtmlSource(bbcUrl, bbcTitle, bbcBody, 'utf-8')
# host = input("NNTP host: ") #freenews.netfront.net
# group = input("NNTP group: ") #free.tampon.tim.walz
# source = NntpSource(host, group)
# maxCount = int(input("Max news count: "))
# source.setMaxCount(maxCount)
# agent.addSource(source)
agent.addSource(bbc)
# agent.addDestination(PlainTextDestination())
agent.addDestination(HtmlDestination("test.html"))
agent.distributeNews()