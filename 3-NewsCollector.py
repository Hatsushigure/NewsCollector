from argparse import ArgumentParser
from sys import stdout
from BBCSource import BBCSource
from HtmlDestination import HtmlDestination
from SimpleHtmlSource import SimpleHtmlSource
from NewsDistributor import NewsDistributor
from PlainTextDestination import PlainTextDestination
from NNTPSource import NNTPSource


def main():
    parser = ArgumentParser(
        prog = 'NewsCollector',
        description = "A program to collect news from different sources"
    )
    parser.add_argument("-s", "--source", nargs = '+', required = True,
                        help = "News sources, available values are 'bbc', 'lagacy', and 'nntp'")
    parser.add_argument("-f", "--file", default = None,
                        help = "The file to store result, if not specified, results go to stdout," \
                               "specially, filename with extension 'html' will be stored as real html")
    parser.add_argument("-H", "--host", default = "freenews.netfront.net",
                        help = "NNTP host, default freenews.netfront.net")
    parser.add_argument("-g", "--group", default = "free.tampon.tim.walz",
                        help = "NNTP group, default free.tampon.tim.walz")
    parser.add_argument("-c", "--count", default = 10, type = int,
                        help = "Number of news to collect, default 10 (NNTP only)")
    args = parser.parse_args()

    newsDistributor = NewsDistributor()

    if "nntp" in args.source:
        nntpSource = NNTPSource(args.host, args.group)
        newsDistributor.addSource(nntpSource)
    if "lagacy" in args.source:
        htmlSource = SimpleHtmlSource(
            "https://bbc.com/",
            r'<h2 data-testid="card-headline".*?>(.*?)<.*?/h2>(?:</div>){2}<p data-testid="card-description".*?>.*?</p>',
            r'<h2 data-testid="card-headline".*?>.*?<.*?/h2>(?:</div>){2}<p data-testid="card-description".*?>(.*?)</p>'
        )
        newsDistributor.addSource(htmlSource)
    if "bbc" in args.source:
        bbcSource = BBCSource()
        newsDistributor.addSource(bbcSource)

    if args.file is not None and args.file.endswith(".html"):
        htmlDestination = HtmlDestination(args.file)
        newsDistributor.addDestination(htmlDestination)
    else:
        plainTextDestination = PlainTextDestination(stdout
        if args.file is None else args.file)
        newsDistributor.addDestination(plainTextDestination)

    newsDistributor.distributeNews()


if __name__ == "__main__":
    main()
