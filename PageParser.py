import sys
import urllib2
import bs4
from bs4 import BeautifulSoup
import re


class PageParser:
    def __init__(self, url):
        self.url = url
        self.soup = self.getPage(url)

    def getPage(self, url):
        try:
            page = urllib2.urlopen(url)
            self.soup = BeautifulSoup(page.read(), "html.parser")
        except Exception as error:
            print("Url open error! Please try again")
            sys.exit(1)
        else:
            return self.soup

    def isVisible(self, text):
        if text.parent.name in ['style', 'script', '[document]', 'head']:
            return False
        elif isinstance(text, bs4.element.Comment):
            return False
        return True

    def getAllText(self):
        text = self.soup.findAll(text=True)
        visibleText = filter(self.isVisible, text)
        return ' '.join(visibleText)

    def getTitle(self):
        text = self.soup.title.get_text()
        return text

    def getHeadings(self, number=4):
        headingText = []
        for i in range(1, number + 1):
            heading = "h" + str(i)
            text = []
            results = self.soup.find_all(heading)
            # print results
            for result in results:
                # print(result.get_text())
                text += result.get_text(),
                # print(text)
            headingText += text,
        return headingText
