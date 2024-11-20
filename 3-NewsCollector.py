from BBCSource import BBCSource
from HtmlDestination import HtmlDestination
from SimpleHtmlSource import SimpleHtmlSource
from NewsDistributor import NewsDistributor
from PlainTextDestination import PlainTextDestination
from NNTPSource import NNTPSource


def main():
    nntpSource = NNTPSource("freenews.netfront.net", "free.tampon.tim.walz")
    bbcSource = BBCSource()
    # htmlSource = SimpleHtmlSource(
    #     "https://bbc.com/",
    #     r'<h2 data-testid="card-headline".*?>(.*?)<.*?/h2>(?:</div>){2}<p data-testid="card-description".*?>.*?</p>',
    #     r'<h2 data-testid="card-headline".*?>.*?<.*?/h2>(?:</div>){2}<p data-testid="card-description".*?>(.*?)</p>'
    # )
    newsDistributor = NewsDistributor()
    plainTextDestination = PlainTextDestination("test.txt")
    htmlDestination = HtmlDestination("test.html")
    newsDistributor.addSource(nntpSource)
    # newsDistributor.addSource(htmlSource)
    newsDistributor.addSource(bbcSource)
    (newsDistributor
     .addDestination(plainTextDestination)
     .addDestination(htmlDestination))
    newsDistributor.distributeNews()


if __name__ == "__main__":
    main()
