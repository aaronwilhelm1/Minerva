from article import Article
import cPickle
import os.path
from globals import artFolderName, artFileEnding


class Library():
    def __init__(self):
        # starts off empty but is added to as articles are read from memory
        self.lib = {}

    def addArticle(self, article):
        self.lib[article.getTitle()] = article
        f = open(artFolderName + article.getTitle() + artFileEnding, 'w')
        cPickle.dump(article, f)
        f.close()

    # each time an article is added, it is stored in the hashmap for quick look-up later
    def getArticle(self, articleTitle):
        if articleTitle in self.lib:
            return self.lib[articleTitle]
        else:
            if self.hasArticle(articleTitle):
                f = open(artFolderName + articleTitle + artFileEnding, 'r')
                self.lib[articleTitle] = cPickle.load(f)
                f.close()
                return self.lib[articleTitle]
            else:
                print("ERROR: Could not find an article titled: " + articleTitle)

    def hasArticle(self, articleTitle):
        if articleTitle in self.lib:
            return True
        else:
            return os.path.isfile(artFolderName + articleTitle)

    #prints all of the info at once. Used for debugging purposes
    def dump(self):
        num = 0
        print("Number of Articles: " + str(len(self.lib)))
        for art in self.lib:
            article = self.lib[art]
            print("Article #" + str(num))
            print("Title: " + article.getTitle())
            print("Text:")
            print(article.getText())
            print('\n')
            num = num + 1


# art1 = Article("Title 1", "Text 1")
# art2 = Article("Title 2", "Text 2")
# f = open(artFolderName + art1.getTitle() + artFileEnding, 'w')
# cPickle.dump(art1, f)
# f.close()
# f = open(artFolderName + art2.getTitle() + artFileEnding, 'w')
# cPickle.dump(art2, f)
# f.close()
# myLib = Library()
# assert myLib.hasArticle("Title 1")
# assert myLib.hasArticle("Title 2")
# assert not myLib.hasArticle("Title 3")
# print(myLib.getArticle(art1.getTitle()).getTitle())
# print(myLib.getArticle(art1.getTitle()).getTitle())
# print(myLib.getArticle(art2.getTitle()).getTitle())
# print(myLib.getArticle(art2.getTitle()).getTitle())
# print(myLib.getArticle("Title 3"))
# myLib.dump()
