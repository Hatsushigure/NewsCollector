class HtmlDestination:
    def __init__(self, file, title = "Today's news", encoding="utf-8"):
        self.outFile = open(file, "w", encoding=encoding)
        self.encoding = encoding
        self.title = title

    def receive(self, items):
        print(f"""
<!DOCTYPE html>
<html>
    <head>
        <meta charset="{self.encoding}">
        <title>{self.title}</title>
    </head>
    <body>
        <h1>{self.title}</h1>
        <ul>
""", end = "", file=self.outFile)
        id = 0
        for item in items:
            print(f"""
            <li><a href=#{id}>{item.title}</a> - {item.source}</li>
""", end = "", file=self.outFile)
            id += 1
        print(f"""
        </ul>
""", end = "", file=self.outFile)
        id = 0
        for item in items:
            print(f"""
        <h2 id={id}>{item.title}</h2>
""", end = "", file=self.outFile)
            id += 1
            print(f"""
        <pre>{item.body}</pre>
""", end = "", file=self.outFile)
        print(f"""
    </body>
</html>
""", end = "", file=self.outFile)
