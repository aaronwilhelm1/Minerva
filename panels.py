from Tkinter import *
from library import Library
from article import Article
from os import listdir
from os.path import isfile, join, splitext
from globals import *
import string
from yandexTranslateHandler import getTranslation
from unidecode import unidecode


class Panel(object):
    def __init__(self, masterPanel, controller):
        self.frame = Frame(masterPanel, width=0, height=0)
        self.controller = controller

    def getFrame(self):
        return self.frame


class ImportPanel(Panel):
    def __init__(self, masterPanel, controller):
        super(ImportPanel, self).__init__(masterPanel, controller)
        self.header = Label(self.frame, text="Import")
        self.header.pack()
        self.title = Label(self.frame, text="Title")
        self.title.pack()
        self.titleEntry = Entry(self.frame, bd=5)
        self.titleEntry.pack(fill=X)
        self.textLabel = Label(self.frame, text="Text")
        self.textLabel.pack()
        # make the drop-down menu to select the language
        self.chosenLanguage = StringVar(self.frame)
        self.chosenLanguage.set(languages[0])
        self.languageSelection = OptionMenu(self.frame, self.chosenLanguage, *languages)
        self.languageSelection.pack()
        # make the entry frame
        self.textEntryFrame = Frame(self.frame)
        self.textEntryScrollbar = Scrollbar(self.textEntryFrame)
        self.textEntry = Text(self.textEntryFrame, yscrollcommand=self.textEntryScrollbar.set)
        self.textEntry.pack(side=LEFT, fill=BOTH, expand=1)
        self.textEntryScrollbar.pack(side=RIGHT, fill=Y)
        self.textEntryScrollbar.config(command=self.textEntry.yview)
        self.textEntryFrame.pack(fill=BOTH, expand=1)
        # end the entry frame
        self.add = Button(self.frame, text="Add to Library", command=lambda: self.contentListener("add"))
        self.add.pack()
        self.statusLabel = Label(self.frame)
        self.statusLabel.pack()

    def contentListener(self, action):
        if(action == "add"):
            self.controller.importArticle(Article(self.titleEntry.get(), self.textEntry.get(1.0, END), languageCodes[languages.index(self.chosenLanguage.get())]))
            self.statusLabel.config(text='Success')
            self.titleEntry.delete(0, END)
            self.textEntry.delete(1.0, END)


class ReadPanel(Panel):
    def __init__(self, masterPanel, controller):
        super(ReadPanel, self).__init__(masterPanel, controller)
        self.header = Label(self.frame, text="Read")
        self.header.pack()
        self.title = Label(self.frame, text="Title")
        self.title.pack()
        self.contentFrame = Frame(self.frame)
        # make the text frame
        self.textFrame = Frame(self.contentFrame)
        self.textScrollbar = Scrollbar(self.textFrame)
        self.text = Text(self.textFrame, state=DISABLED, yscrollcommand=self.textScrollbar.set, width=0, wrap=WORD, font=("Helvetica", 14), cursor="arrow")
        # self.text.pack(fill=X)
        self.text.pack(side=LEFT, fill=BOTH, expand=1)
        #set up the tag so that clicked words are registered
        self.text.tag_config("all", background="yellow")
        self.text.tag_bind("all", "<Button-1>", self.textClickHandler)
        self.text.tag_config("title", font=("Helvetica", 16, "bold"))
        self.text.tag_config("text")
        self.text.tag_config(SEL, foreground="black")
        self.text.tag_raise(SEL)
        self.textScrollbar.pack(side=LEFT, fill=Y)
        self.textScrollbar.config(command=self.text.yview)
        self.textFrame.grid(row=0, column=0, rowspan=6, columnspan=6, sticky=N+S+E+W)
        # end the text frame
        # make the content for to display word info
        self.selectedWord = Label(self.contentFrame, width=0, font=("Helvetica", 18), text="Word", pady=5)
        self.display = Text(self.contentFrame, width=0, wrap=WORD, font=("Helvetica", 16))
        self.addButton = Button(self.contentFrame, text="Add", command=lambda: self.contentListener("addTranslation"))
        self.refetchButton = Button(self.contentFrame, text="Refetch", command=lambda: self.contentListener("refetch"))
        self.selectedWord.grid(row=0, column=6, rowspan=1, columnspan=2, sticky=N+S+E+W)
        self.display.grid(row=1, column=6, rowspan=4, columnspan=2, sticky=N+S+E+W)
        self.addButton.grid(row=5, column=6, sticky=N+S+E+W)
        self.refetchButton.grid(row=5, column=7, sticky=N+S+E+W)
        for c in range(8):
            Grid.columnconfigure(self.contentFrame, c, weight=1)
        for r in range(6):
            Grid.rowconfigure(self.contentFrame, r, weight=1)
        self.contentFrame.pack(fill=BOTH, expand=1)

    #create a listener for the readable text
    def textClickHandler(self, evt):
        # get the index of the mouse click
        index = evt.widget.index("@%s,%s" % (evt.x, evt.y))
        startOfWord = "%swordstart" % index
        endOfWord = "%swordend" % index
        word = self.text.get(startOfWord, endOfWord)
        translations = getTranslation(word, self.language, "en")
        self.display.delete(1.0, END)
        if len(translations) == 0:
            self.display.insert(END, translate_error_message(word))
        else:
            self.display.insert(END, self.translationToString(translations))

    def translationToString(self, translations):
        toReturn = ""
        for type in translations:
            toReturn += type[0]
            if(type[2] is not None):
                toReturn += " (" + type[2] + ")"
            if(type[3] is not None):
                toReturn += " -" + type[3]
            if(type[4] is not None):
                toReturn += " -" + type[4]
            toReturn += "\n"
            for definition in range(len(type[1])):
                toReturn += "   " + str(definition + 1) + ".) "
                for syn in range(len(type[1][definition])):
                    toReturn += type[1][definition][syn]
                    if not syn == (len(type[1][definition]) - 1):
                        toReturn += ", "
                    else:
                        toReturn += "\n"
                toReturn += "\n"
        return toReturn

    def displayArticle(self, article):
        try:
            self.language = article.getLanguage()
        except AttributeError:
            self.language = languageCodes[0]
        self.title.config(text=article.getTitle())
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(1.0, article.getTitle() + "\n\n", "title")
        self.text.insert(END, article.getText(), "text")
        self.text.config(state=DISABLED)
        index = 1.0
        lastChar = self.text.index("%s-1c" % END)
        while(index != lastChar):
            character = self.text.get(index)
            if self.isMeaningfulCharacter(character) is True:
                self.text.tag_add("all", index, "%swordend" % index)
                index = self.text.index("%swordend" % index)
            index = self.text.index("%s+1c" % index)

    def isMeaningfulCharacter(self, char):
        character = unidecode(char)
        if any(c in character for c in string.punctuation + string.whitespace):
            return False
        else:
            return True

    def contentListener(self, action):
        #TODO: Replace with valid listeners
        print("Content listener for read panel was called but nothing is here yet!")


class SelectPanel(Panel):
    def __init__(self, masterPanel, controller):
        super(SelectPanel, self).__init__(masterPanel, controller)
        self.header = Label(self.frame, text="Make A Selection")
        self.header.pack()
        # make the selection container frame
        self.selectionContainerFrame = Frame(self.frame)
        self.selectionsScrollbar = Scrollbar(self.selectionContainerFrame)
        self.selections = Listbox(self.selectionContainerFrame, selectmode=SINGLE, name='selections')
        self.selections.bind('<<ListboxSelect>>', self.onselect)
        onlyfiles = [f for f in listdir(artFolderName) if isfile(join(artFolderName, f)) and f.endswith(artFileEnding)]
        for articleTitle in onlyfiles:
            self.selections.insert(END, splitext(articleTitle)[0])
        self.selections.pack(side=LEFT, fill=BOTH, expand=1)
        self.selectionsScrollbar.pack(side=RIGHT, fill=Y)
        self.selectionsScrollbar.config(command=self.selections.yview)
        self.selectionContainerFrame.pack(fill=BOTH, expand=1)
        # end the selection container frame

    def addSelection(self, articleTitle):
        self.selections.insert(END, articleTitle)

    def onselect(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.controller.articleSelected(value)
