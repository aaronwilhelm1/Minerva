#from article import Article


class Library():
    def __init__(self):
        self.lib = {}
        # art1 = Article("Title 1", "Text 1")
        # art2 = Article("Title 2", "Text 2")
        # self.lib[art1.getTitle()] = art1
        # self.lib[art2.getTitle()] = art2

    def addArticle(self, article):
        self.lib[article.getTitle()] = article

    def getArticle(self, articleTitle):
        return self.lib[articleTitle]

    def hasArticle(self, articleTitle):
        return articleTitle in self.lib

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

# myLib = Library()
# myLib.dump()
