from html.parser import HTMLParser
from urllib.request import urlopen
from NewsItem import NewsItem


class BBCSource(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inCard = False
        self.cardDepth = 0
        self.inTitle = False
        self.inContent = False
        self.titles = []
        self.bodies = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div" and not self.inCard:
            if "data-testid" in attrs and attrs["data-testid"] == "card-text-wrapper":
                self.inCard = True
                return
        if not self.inCard:
            return
        self.cardDepth += 1
        if "data-testid" in attrs and attrs["data-testid"] == "card-headline":
            self.inTitle = True
        elif "data-testid" in attrs and attrs["data-testid"] == "card-description":
            self.inContent = True

    def handle_endtag(self, tag):
        if not self.inCard:
            return
        if tag == "div" and self.cardDepth == 0:
            self.inCard = False
        else:
            self.cardDepth -= 1
        if tag == "h2" and self.inTitle:
            self.inTitle = False
        if self.inContent:
            self.inContent = False

    def handle_data(self, data):
        if self.inTitle:
            self.titles.append(data)
        elif self.inContent:
            self.bodies.append(data)

    def getItems(self):
        self.feed(urlopen("https://bbc.com/").read().decode("utf-8"))
        for title, body in zip(self.titles, self.bodies):
            yield NewsItem(title, body, "https://bbc.com/")
        # print(len(self.titles))
        # print(len(self.bodies))


source = BBCSource()
source.getItems()
