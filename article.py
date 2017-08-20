

#A data container for the articles
class Article():
    def __init__(self, title, text):
        self.title = title
        self.text = text

    def getTitle(self):
        return self.title

    def getText(self):
        return self.text
