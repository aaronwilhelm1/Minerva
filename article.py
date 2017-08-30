

# A data container for the articles
# The language should be the 2 letter language code as outlined in globals
class Article():
    def __init__(self, title, text, language):
        self.title = title
        self.text = text
        self.language = language

    def getTitle(self):
        return self.title

    def getText(self):
        return self.text

    def getLanguage(self):
        return self.language
