from nntplib import NNTP, decode_header
from NewsItem import NewsItem


class NNTPSource:
    def __init__(self, host, group, maxCount=10):
        self.host = host
        self.group = group
        self.maxCount = maxCount

    def getHost(self):
        return self.host

    def setHost(self, host):
        self.host = host
        return self

    def getGroup(self):
        return self.group

    def setGroup(self, group):
        self.group = group
        return self

    def getMaxCount(self):
        return self.maxCount

    def setMaxCount(self, maxCount):
        self.maxCount = maxCount
        return self

    def getItems(self):
        server = NNTP(self.host)
        resp, count, first, last, name = server.group(self.group)
        if count < self.maxCount:
            self.maxCount = count
        resp, overviews = server.over((last - self.maxCount + 1, last))
        for newsId, overview in overviews:
            title = decode_header(overview["subject"])
            resp, info = server.body(newsId)
            body = "\n".join(line.decode("latin") for line in info.lines)
            yield NewsItem(title, body, self.host + " (NNTP)")
        server.quit()
