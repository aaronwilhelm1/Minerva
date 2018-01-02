#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from article import Article
from os import listdir
from os.path import isfile, join, splitext
from globals import *
import string
from hybridTranslateHandler import getTranslation
from unidecode import unidecode
import cPickle
from wordlist import WordList


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
        self.titleEntry = Entry(self.frame, bd=5, font=("Helvetica", 12))
        self.titleEntry.pack(fill=X)
        self.textLabel = Label(self.frame, text="Text", font=("Helvetica", 14))
        self.textLabel.pack()
        # make the drop-down menu to select the language
        self.chosenLanguage = StringVar(self.frame)
        self.chosenLanguage.set(languages[0])
        self.languageSelection = OptionMenu(self.frame, self.chosenLanguage, *languages)
        self.languageSelection.pack()
        # make the entry frame
        self.textEntryFrame = Frame(self.frame)
        self.textEntryScrollbar = Scrollbar(self.textEntryFrame)
        self.textEntry = Text(self.textEntryFrame, yscrollcommand=self.textEntryScrollbar.set, wrap=WORD, font=("Helvetica", 14))
        self.textEntry.pack(side=LEFT, fill=BOTH, expand=1)
        self.textEntryScrollbar.pack(side=RIGHT, fill=Y)
        self.textEntryScrollbar.config(command=self.textEntry.yview)
        self.textEntry.bind("<Button-1>", self.textLeftClickHandler)
        self.haveClicked = False
        self.textEntry.insert(END, import_hint)
        # end the entry frame
        self.add = Button(self.frame, text="Add to Library", command=lambda: self.contentListener("add"))
        self.add.pack(side=BOTTOM)
        # pack the text entry frame so it doesn't swell up too big
        self.textEntryFrame.pack(fill=BOTH, expand=1)
        self.statusLabel = Label(self.frame)
        self.statusLabel.pack()

    def contentListener(self, action):
        if(action == "add"):
            self.controller.importArticle(Article(self.titleEntry.get(), self.textEntry.get(1.0, END), languageCodes[languages.index(self.chosenLanguage.get())]))
            self.statusLabel.config(text='Success')
            self.titleEntry.delete(0, END)
            self.textEntry.delete(1.0, END)

    def textLeftClickHandler(self, evt):
        if self.haveClicked is False:
            self.textEntry.delete(1.0, END)
            self.haveClicked = True
            self.textEntry["font"] = ("Helvetica", 12)


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
        self.text.tag_config("all")
        self.text.tag_bind("all", "<Button-1>", self.textLeftClickHandler)
        self.text.tag_bind("all", "<Button-3>", self.textRightClickHandler)
        self.text.tag_config("title", font=("Helvetica", 16, "bold"))
        self.text.tag_config("text")
        self.text.tag_config("new", background="gold")
        self.text.tag_config("learning", background="steel blue")
        self.text.tag_config("known")
        self.text.tag_config(SEL, foreground="black", background="chartreuse4")
        self.text.tag_raise(SEL)
        self.textScrollbar.pack(side=LEFT, fill=Y)
        self.textScrollbar.config(command=self.text.yview)
        self.textFrame.grid(row=0, column=0, rowspan=6, columnspan=6, sticky=N+S+E+W)
        # end the text frame
        # make the content for to display word info
        self.selectedWord = Label(self.contentFrame, width=0, font=("Helvetica", 18), text="Word", pady=5)
        self.display = Text(self.contentFrame, width=0, wrap=WORD, font=("Helvetica", 16))
        self.addButton = Button(self.contentFrame, text="Add/Save", command=lambda: self.contentListener("addTranslation"))
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
        # Set the learning lists to None since no language has been chosen yet (and they could try to save it)
        self.learning = None
        self.known = None

    #create a listener for the readable text
    def textLeftClickHandler(self, evt):
        # get the index of the mouse click
        index = evt.widget.index("@%s,%s" % (evt.x, evt.y))
        startOfWord = "%swordstart" % index
        endOfWord = "%swordend" % index
        word = self.text.get(startOfWord, endOfWord).lower()
        if self.learning.hasWord(word):
            translation = self.learning.getTranslation(word)
        elif self.known.hasWord(word):
            translation = self.known.getTranslation(word)
        else:
            # We have never seen this word before
            translationObj = getTranslation(word, self.language, "en")
            translation = self.translationToString(translationObj)
            if len(translation) == 0:  # Couldn't get anything
                translation = translate_error_message(word)
        self.display.delete(1.0, END)
        self.display.insert(END, translation)
        self.lastLeftClickedIndex = index

    #create a listener for the readable text
    def textRightClickHandler(self, evt):
        # get the index of the mouse click
        index = evt.widget.index("@%s,%s" % (evt.x, evt.y))
        tags = self.text.tag_names(index)
        startOfWord = "%swordstart" % index
        endOfWord = "%swordend" % index
        word = self.text.get(startOfWord, endOfWord).lower()
        if "new" in tags:
            self.known.addWord(word, have_not_translated_message(word))
            self.text.tag_add("known", startOfWord, endOfWord)
            self.updateTags(word, "new", "known")
        elif "learning" in tags:
            self.known.addWord(word, self.learning.getTranslation(word))
            self.learning.deleteWord(word)
            self.text.tag_add("known", startOfWord, endOfWord)
            self.updateTags(word, "learning", "known")
        else:
            # Word must be known, so put it back into learning words
            self.learning.addWord(word, self.known.getTranslation(word))
            self.known.deleteWord(word)
            self.text.tag_add("learning", startOfWord, endOfWord)
            self.updateTags(word, "known", "learning")

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
        # Setup the word lists
        if isfile(wlFolderName + self.language + "learning" + wlFileEnding):
            f = open(wlFolderName + self.language + "learning" + wlFileEnding, 'r')
            self.learning = cPickle.load(f)
            f.close()
        else:
            self.learning = WordList("learning", self.language)
        if isfile(wlFolderName + self.language + "known" + wlFileEnding):
            f = open(wlFolderName + self.language + "known" + wlFileEnding, 'r')
            self.known = cPickle.load(f)
            f.close()
        else:
            self.known = WordList("known", self.language)
        # Clear the last clicked index since no word has been clicked yet
        self.lastLeftClickedIndex = None
        # Setup the displays
        self.title.config(text=article.getTitle())
        self.display.delete(1.0, END)
        self.display.insert(1.0, read_display_intro)
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
                endOfWord = "%swordend" % index
                word = self.text.get(index, endOfWord).lower()
                # Ignore if it is a digit
                if not word.isdigit():
                    self.text.tag_add("all", index, endOfWord)
                    if self.learning.hasWord(word):
                        self.text.tag_add("learning", index, endOfWord)
                    elif self.known.hasWord(word):
                        self.text.tag_add("known", index, endOfWord)
                    else:
                        self.text.tag_add("new", index, endOfWord)
                index = self.text.index("%swordend" % index)
            index = self.text.index("%s+1c" % index)

    def isMeaningfulCharacter(self, char):
        character = unidecode(char)
        if any(c in character for c in string.punctuation + string.whitespace + u"„“"):
            return False
        else:
            return True

    def contentListener(self, action):
        if action == "addTranslation":
            if self.lastLeftClickedIndex is not None:
                index = self.lastLeftClickedIndex
                startOfWord = "%swordstart" % index
                endOfWord = "%swordend" % index
                word = self.text.get(startOfWord, endOfWord).lower()
                if self.learning.hasWord(word):
                    self.learning.setTranslation(word, self.display.get(1.0, END))
                else:
                    self.learning.addWord(word, self.display.get(1.0, END))
                    if self.known.hasWord(word):
                        # know it was a known word
                        self.known.deleteWord(word)
                        self.updateTags(word, "known", "learning")
                    else:
                        # know it was a new word
                        self.updateTags(word, "new", "learning")
        elif action == "refetch":
            if self.lastLeftClickedIndex is not None:
                index = self.lastLeftClickedIndex
                startOfWord = "%swordstart" % index
                endOfWord = "%swordend" % index
                word = self.text.get(startOfWord, endOfWord).lower()
                translationObj = getTranslation(word, self.language, "en")
                translation = self.translationToString(translationObj)
                if len(translation) == 0:  # Couldn't get anything
                    translation = translate_error_message(word)
                self.display.delete(1.0, END)
                self.display.insert(END, translation)

    # goes through the text making every instance of the word the new tag
    def updateTags(self, word, prevTag, newTag):
        index = 1.0
        result = self.text.tag_nextrange(prevTag, index)
        while(len(result) != 0):
            startOfWord, endOfWord = result
            foundWord = self.text.get(startOfWord, endOfWord).lower()
            if word.lower() == foundWord:
                self.text.tag_remove(prevTag, startOfWord, endOfWord)
                self.text.tag_add(newTag, startOfWord, endOfWord)
            index = self.text.index("%s+1c" % endOfWord)
            result = self.text.tag_nextrange(prevTag, index)

    def saveWordLists(self):
        if self.learning is not None:
            self.learning.saveWordList()
        if self.known is not None:
            self.known.saveWordList()


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


class StatsPanel(Panel):
    def __init__(self, masterPanel, controller):
        super(StatsPanel, self).__init__(masterPanel, controller)
        self.header = Label(self.frame, text="Statistics")
        self.header.pack()
        # make the selection container frame
        self.statsContainerFrame = Frame(self.frame)
        self.statsScrollbar = Scrollbar(self.statsContainerFrame)
        self.statsScrollbar.pack(side=RIGHT, fill=Y)
        # self.statsScrollbar.config(command=self.statsContainerFrame.yview)
        self.statsContainerFrame.pack(fill=BOTH, expand=1)

    # Override the parent method since we need to dynamically generate this (# of languages can change)
    def getFrame(self):
        onlyfiles = [f for f in listdir(wlFolderName) if isfile(join(wlFolderName, f)) and f.endswith(wlFileEnding)]
        langCodes = []
        for file in onlyfiles:
            langCode = file[0:2]
            if langCode not in langCodes:
                langCodes.append(langCode)
        # convert each of the languageCodes to their readable text form
        langs = []
        for langCode in langCodes:
            langs.append(languages[languageCodes.index(langCode)])
        labels = self.statsContainerFrame.winfo_children()
        for lab in labels:
            lab.destroy()
        for x in range(len(langs)):
            f = open(wlFolderName + langCodes[x] + "learning" + wlFileEnding, 'r')
            learning = cPickle.load(f)
            f.close()
            f = open(wlFolderName + langCodes[x] + "known" + wlFileEnding, 'r')
            known = cPickle.load(f)
            f.close()
            learningLabel = Label(self.statsContainerFrame, text="# of Words in " + langs[x] + u" Learning List\u00ae:", borderwidth=5, relief="solid", font=("Helvetica", 16))
            learnNum = Label(self.statsContainerFrame, text=str(learning.getSize()), borderwidth=5, relief="solid", font=("Helvetica", 16))
            knownLabel =  Label(self.statsContainerFrame, text="# of Words in " + langs[x] + u" Known List:", borderwidth=5, relief="solid", font=("Helvetica", 16))
            knownNum = Label(self.statsContainerFrame, text=str(known.getSize()), borderwidth=5, relief="solid", font=("Helvetica", 16))
            learningLabel.grid(row=(x * 2), column=0, sticky=N+S+E+W)
            learnNum.grid(row=(x * 2), column=1, sticky=N+S+E+W)
            knownLabel.grid(row=((x * 2) + 1), column=0, sticky=N+S+E+W)
            knownNum.grid(row=((x * 2) + 1), column=1, sticky=N+S+E+W)
        for c in range(2):
            Grid.columnconfigure(self.statsContainerFrame, c, weight=1)
        for r in range(len(langs) * 2):
            Grid.rowconfigure(self.statsContainerFrame, r, weight=1)
        return super(StatsPanel, self).getFrame()
