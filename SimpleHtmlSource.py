from urllib.request import urlopen
from NewsItem import NewsItem
import re


class SimpleHtmlSource:
    def __init__(self, url, titleRegex, bodyRegex, encoding="utf-8"):
        self.url = url
        self.titleRegex = re.compile(titleRegex)
        self.bodyRegex = re.compile(bodyRegex)
        self.encoding = encoding

    def getItems(self):
        html = urlopen(self.url).read().decode(self.encoding)
        titles = self.titleRegex.findall(html)
        bodies = self.bodyRegex.findall(html)
        for title, body in zip(titles, bodies):
            yield NewsItem(title, body, self.url)
