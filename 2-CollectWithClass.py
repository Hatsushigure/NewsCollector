from nntplib import NNTP

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

class NNTPSource:
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

class PlainTextDestination:
    def receive(self, items):
        for item in items:
            print(item.title)
            print(item.body)

agent = NewsAgent()
host = input("NNTP host: ") #freenews.netfront.net
group = input("NNTP group: ") #free.tampon.tim.walz
source = NNTPSource(host, group)
maxCount = int(input("Max news count: "))
source.setMaxCount(maxCount)
agent.addSource(source)
agent.addDestination(PlainTextDestination())
agent.distributeNews()