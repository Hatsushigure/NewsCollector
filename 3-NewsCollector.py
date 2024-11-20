from SimpleHtmlSource import SimpleHtmlSource
from NewsDistributor import NewsDistributor
from PlainTextDestination import PlainTextDestination
from NNTPSource import NNTPSource


def main():
    nntpSource = NNTPSource("freenews.netfront.net", "free.tampon.tim.walz")
    htmlSource = SimpleHtmlSource(
        "https://bbc.com/",
        r'<h2 data-testid="card-headline".*?>(.*?)<.*?/h2>(?:</div>){2}<p data-testid="card-description".*?>.*?</p>',
        r'<h2 data-testid="card-headline".*?>.*?<.*?/h2>(?:</div>){2}<p data-testid="card-description".*?>(.*?)</p>'
    )
    newsDistributor = NewsDistributor()
    plainTextDestination = PlainTextDestination("test.txt")
    newsDistributor.addSource(nntpSource)
    newsDistributor.addSource(htmlSource)
    newsDistributor.addDestination(plainTextDestination)
    newsDistributor.distributeNews()


if __name__ == "__main__":
    main()
