import cPickle
from globals import wlFolderName, wlFileEnding


# A data container for the words
class WordData():
    def __init__(self, word, translation):
        self.word = word
        self.translation = translation
        self.count = 0
        self.articles = []

    def getWord(self):
        return self.word

    def getTranslation(self):
        return self.translation

    def getCount(self):
        return self.count

    def getArticles(self):
        return self.articles

    def setTranslation(self, newTranslation):
        self.translation = newTranslation

    def setCount(self, newCount):
        self.count = newCount


class WordList():
    def __init__(self, wordListName, language):
        self.words = {}
        self.name = wordListName
        self.language = language

    def addWord(self, word, translation):
        self.words[word] = WordData(word, translation)

    def deleteWord(self, word):
        del self.words[word]

    def hasWord(self, word):
        return word in self.words

    def getTranslation(self, word):
        return self.words[word].getTranslation()

    def getCount(self, word):
        return self.words[word].getCount()

    def getArticles(self, word):
        return self.words[word].getArticles()

    def getLanguage(self, language):
        return self.language

    def getSize(self):
        return len(self.words)

    def setTranslation(self, word, newTranslation):
        self.words[word].setTranslation(newTranslation)

    def setCount(self, word, newCount):
        self.words[word].setCount(newCount)

    def addArticle(self, word, articleTitle):
        self.words[word].getArticles().append(articleTitle)

    def saveWordList(self):
        f = open(wlFolderName + self.language + self.name + wlFileEnding, 'w')
        cPickle.dump(self, f)
        f.close()

    # prints the contents of the word list. Used for debugging purposes
    def dump(self):
        print("Values for Word List " + self.name)
        for word, wd in self.words.iteritems():
            print(wd.getWord() + ":")
            print("Translation: " + wd.getTranslation() + " Count: " + str(wd.getCount()))
            print("Articles: " + str(wd.getArticles()))
            print("----------")
        print("xxxxxxxxxxxxxxxxxxxxxxxx")
        print("")


# wl = WordList("testWordList", "en")
# wl.addWord("first", "erst")
# wl.addWord("second", "zweite")
# wl.addArticle("first", "The title of the first article")
# wl.addArticle("first", "The second article")
# wl.setCount("first", 2)
# wl.addArticle("second", "The First article")
# assert wl.hasWord("first")
# assert not wl.hasWord("third")
# wl.setTranslation("second", "newTranslation")
# wl.dump()
# wl.getArticles("first").pop()
# wl.dump()
# wl.saveWordList()
# print("Just saved the word list. Now reloading it")
# f = open(wlFolderName + "en" "testWordList" + wlFileEnding, 'r')
# wlNew = cPickle.load(f)
# f.close()
# wlNew.dump()
# print(wl.getSize())
