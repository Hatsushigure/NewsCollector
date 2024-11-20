class NewsDistributor:
    def __init__(self):
        self.sources = []
        self.destinations = []

    def addSource(self, source):
        self.sources.append(source)
        return self

    def addDestination(self, destination):
        self.destinations.append(destination)
        return self

    def distributeNews(self):
        items = []
        for source in self.sources:
            items.extend(source.getItems())
        for destination in self.destinations:
            destination.receive(items)
