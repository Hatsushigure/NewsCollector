from sys import stdout


class PlainTextDestination:
    def __init__(self, file=stdout):
        self.outFile = open(file, "w", encoding="utf-8")

    def receive(self, items):
        for item in items:
            print(f"{item.title} - {item.source}", file=self.outFile)
            print("-" * len(item.title), file=self.outFile)
            print(item.body + "\n", file=self.outFile)
