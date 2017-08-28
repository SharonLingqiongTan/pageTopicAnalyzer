import re
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from collections import Counter


class PageTopicAnalyzer:
    def __init__(self, text="", deli=None, lem=False, stem=False, low=True, stopWord=None):
        self.stopWords = self.seoSW('seoSW.txt')
        # print(self.stopWords)
        self.delimiters = [",", "\.", ":", ";", "\?", "&"]
        self.wordCount = {}
        self.bagOfWords = []
        # print(self.stopWords)
        if stopWord:
            stopSet = set(self.stopWords)
            for word in stopWord:
                if word.startswith('-'):
                    try:
                        stopSet.remove(word[1:].lower())
                    except:
                        pass
                else:
                    stopSet.add(word)
            self.stopWords = list(stopSet)

        if deli:
            deliSet = set(self.delimiters)
            for item in deli:
                if item.startswith('-') and len(item) < 2:  # special case: "-"
                    try:
                        deliSet.remove(item[1:])
                    except:
                        pass
                else:
                    deliSet.add(item)
            self.delimiters = list(deliSet)
        else:
            self.delimiters = self.delimiters
        # print(self.delimiters)
        strings = re.split("|".join(self.delimiters), text)
        for item in strings:
            self.bagOfWords += item.split(),

        lemmatizer = WordNetLemmatizer()
        stemmer = PorterStemmer()
        swDict = Counter(self.stopWords)
        # print(swDict)
        for index,item in enumerate(self.bagOfWords):
            # print(self.bagOfWords)
            self.bagOfWords[index] = filter(lambda x: x.lower() not in swDict, self.bagOfWords[index])
            for i, word in enumerate(self.bagOfWords[index]):
                if lem:
                    item[i] = lemmatizer.lemmatize(word, 'v')
                if stem:
                    item[i] = stemmer.stem(word)
                if low:
                    item[i] = word.lower()

    def seoSW(self, path):
        f = open(path, 'r')
        sw = set(stopwords.words('english'))
        for line in f.readlines():
            sw.add(line.strip())
        return list(sw)

    def __add__(self, other):
        newStopWords = list(set(self.stopWords + other.stopWords))
        newDelimiters = list(set(self.delimiters + other.delimiters))
        newWordCount = self.wordCount + other.wordCount
        newBoW = self.bagOfWords + other.bagOfWords
        newAnalyzer = PageTopicAnalyzer()
        newAnalyzer.stopWords = newStopWords
        newAnalyzer.delimiters = newDelimiters
        newAnalyzer.wordCount = newWordCount
        return newAnalyzer

    def rank(self, top):
        return sorted(self.wordCount, key=self.wordCount.get)[:top]

    def unigram(self):
        words = [y for x in self.bagOfWords for y in x]
        counter = Counter(words)
        self.wordCount = counter
        return self.wordCount

    def bigram(self):
        counter = Counter()
        for item in self.bagOfWords:
            words = [(item[i], item[i + 1]) for i in range(len(item) - 1) if len(item[i]) + len(item[i + 1]) > 2]
            counter += Counter(words)
        self.wordCount = counter
        return self.wordCount

    def uni_bi_gram(self, unigrams, bigrams):
        counter = Counter()
        most_common_uni = unigrams.most_common(10)
        most_common_bi = bigrams.most_common(10)
        # print(most_common_uni, most_common_bi)
        for uni in most_common_uni:
            for bi in most_common_bi:
                if uni[0] in bi[0]:
                    counter[bi[0]] = min(uni[1], bi[1])
        uni_bi_grams = (unigrams + bigrams)
        for uni_bi in uni_bi_grams.most_common(10):
            if uni_bi[0] not in counter:
                counter[uni_bi[0]] = uni_bi[1]
        self.wordCount = counter
        return self.wordCount

    def weighted(self, weight):
        counter = Counter()
        for i in range(weight):
            counter += self.wordCount
        self.wordCount = counter
