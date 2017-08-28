import sys
from PageParser import PageParser
from PageTopicAnalyzer import PageTopicAnalyzer

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('UTF8')
    if len(sys.argv) < 2:
        print("URL missing! Please try again.")
    elif len(sys.argv) > 2:
        print("The program takes exactly one argument. Two received. Please try again.")
    else:
        url = sys.argv[1]
        parser = PageParser(url)
        allText = parser.getAllText()
        # print(allText)
        titleText = parser.getTitle()
        # print(titleText)
        headingText = parser.getHeadings()
        # print(headingText)

        allAnalyzer = PageTopicAnalyzer(allText)
        # print(allAnalyzer.bagOfWords)
        titleAnalyzer = PageTopicAnalyzer(titleText)
        # print(titleAnalyzer.bagOfWords)

        ## Unigram ##
        allAnalyzer.unigram()
        titleAnalyzer.bigram()
        titleAnalyzer.weighted(20)
        # print(titleAnalyzer.wordCount)
        uni_analyzer = allAnalyzer + titleAnalyzer
        # print(analyzer.wordCount)
        ## Bigram ##
        allAnalyzer.bigram()
        titleAnalyzer.bigram()
        titleAnalyzer.weighted(20)
        bi_analyzer = allAnalyzer + titleAnalyzer
        weight = 5
        for i in range(len(headingText)):
            headings = headingText[i]
            for heading in headings:
                headingAnalyzer = PageTopicAnalyzer(heading)
                headingAnalyzer.unigram()
                headingAnalyzer.weighted(weight)
                uni_analyzer += headingAnalyzer
                headingAnalyzer.bigram()
                headingAnalyzer.weighted(weight)
                bi_analyzer += headingAnalyzer
            if i % 2:
                weight -= 1
        analyzer = uni_analyzer + bi_analyzer
        analyzer.uni_bi_gram(uni_analyzer.wordCount, bi_analyzer.wordCount)
        # print(analyzer.wordCount)
        print(analyzer.rank(5))


