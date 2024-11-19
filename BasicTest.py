from nntplib import NNTP
import datetime

address = "nntp.perl.org"
newsCount = 10
server = NNTP(address)
print(server.getwelcome())
resp, count, first, last, name = server.group("perl.daily-build.reports")
print(resp)
resp, overviews = server.over((last - newsCount + 1, last))
for newsId, over in overviews:
    subject = over["subject"]
    resp, info = server.body(newsId)
    print(subject)
    print('-' * len(subject))
    for line in info.lines:
        print(line.decode(server.encoding))
    print()
server.quit()