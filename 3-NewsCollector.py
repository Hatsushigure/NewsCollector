from NewsDistributor import NewsDistributor
from PlainTextDestination import PlainTextDestination
from NNTPSource import NNTPSource


def main():
    nntpSource = NNTPSource("freenews.netfront.net", "free.tampon.tim.walz")
    newsDistributor = NewsDistributor()
    plainTextDestination = PlainTextDestination("test.txt")
    newsDistributor.addSource(nntpSource)
    newsDistributor.addDestination(plainTextDestination)
    newsDistributor.distributeNews()


if __name__ == '__main__':
    main()
