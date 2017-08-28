import sys
import urllib2
from bs4 import BeautifulSoup


class HTMLParser:
    def __init__(self, url):
        self.url = url
        self.soup = self.getPage(url)

    def getPage(self, url):
        try:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page.read(), "html.parser")
        except Exception as error:
            print("Url open error! Please try again")
            sys.exit(1)
        else:
            return soup

    def getAllText(self):
        return self.soup.get_text()

    def getTitle(self):
        return self.soup.title.get_text()

    def getHeadings(self, number=4):
        headingText = []
        for i in range(1, number + 1):
            heading = "h" + str(i)
            text = []
            results = soup.find_all(heading)
            for result in results:
                text += result.get_text()
            headingText += text,
        return headingText
