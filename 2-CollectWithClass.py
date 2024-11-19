import re
import textwrap
from nntplib import NNTP
from urllib.request import urlopen
from argparse import ArgumentParser, Namespace


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
</html>""", file=out)


def runDefaultSetup(args: Namespace):
    agent = NewsAgent()
    bbcUrl = 'https://bbc.com'
    bbcTitle = r'<h2 data-testid="card-headline".*?>(.*?)<.*?/h2>(?:</div>){2}<p data-testid="card-description".*?>.*?</p>'
    bbcBody = r'<h2 data-testid="card-headline".*?>.*?<.*?/h2>(?:</div>){2}<p data-testid="card-description".*?>(.*?)</p>'
    bbc = SimpleHtmlSource(bbcUrl, bbcTitle, bbcBody, 'utf-8')
    nntpHost = args.host  # freenews.netfront.net
    nntpGroup = args.group  # free.tampon.tim.walz
    nntpSource = NntpSource(nntpHost, nntpGroup)
    maxCount = args.count
    nntpSource.setMaxCount(maxCount)
    for sourceName in args.source:
        if sourceName == 'bbc':
            agent.addSource(bbc)
        elif sourceName == 'nntp':
            agent.addSource(nntpSource)
        else:
            print("Unknown source \"{}\"".format(sourceName))
            return
    if args.file is None:
        agent.addDestination(PlainTextDestination())
    else:
        agent.addDestination(HtmlDestination(args.file))
    agent.distributeNews()


if __name__ == '__main__':
    parser = ArgumentParser(
        prog='NewsCollector',
        description="A program to collect news from different sources"
    )
    parser.add_argument("-s", "--source", nargs='+', required=True,
                        help="News sources, available values are 'bbc' and 'nntp'")
    parser.add_argument("-f", "--file", default=None,
                        help="The file to store result, if not specified, results go to stdout")
    parser.add_argument("-H", "--host", default="freenews.netfront.net",
                        help="NNTP host, default freenews.netfront.net")
    parser.add_argument("-g", "--group", default="free.tampon.tim.walz",
                        help="NNTP group, default free.tampon.tim.walz")
    parser.add_argument("-c", "--count", default=10, type=int, help="Number of news to collect, default 10 (NNTP only)")
    args = parser.parse_args()
    runDefaultSetup(args)
