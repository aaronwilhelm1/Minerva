from Tkinter import Tk, Label, Button, Frame, Entry, Text, X, END, Listbox, SINGLE, NORMAL, DISABLED, Scrollbar, RIGHT, Y, BOTH, LEFT, WORD, Grid, N, S, E, W, SEL
from library import Library
from article import Article
from os import listdir
from os.path import isfile, join, splitext
from globals import artFolderName, artFileEnding, translate_error_message
import string
from yandexTranslateHandler import getTranslation
from unidecode import unidecode


def isMeaningfulCharacter(char):
    character = unidecode(char)
    if any(c in character for c in string.punctuation + string.whitespace):
        return False
    else:
        return True


class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Minerva")

        self.canvas_width = self.master.winfo_screenwidth() - 200
        self.canvas_height = self.master.winfo_screenheight() - 200

        self.menu = Frame(master)
        self.menu.grid(row=0, column=0)

        self.content = Frame(master, width=self.canvas_width, height=self.canvas_height)
        self.content.grid(row=0, column=1, columnspan=4)

        #Setup the menu bar
        self.menuLabel = Label(self.menu, text="Menu")
        self.menuLabel.pack()
        self.importButton = Button(self.menu, text="Import", command=lambda: self.update("import"))
        self.importButton.pack()
        self.readButton = Button(self.menu, text="Read", command=lambda: self.update("select"))
        self.readButton.pack()
        self.reviewButton = Button(self.menu, text="Review", command=lambda: self.update("review"))
        self.reviewButton.pack()
        self.statsButton = Button(self.menu, text="Stats", command=lambda: self.update("stats"))
        self.statsButton.pack()

        #Setup the possible content pages
        self.setupImport()
        self.setupRead()
        self.setupSelect()

        #default to the import page
        self.status = "import"
        self.update("import")

        self.lib = Library()

    def update(self, method):
        #remove the old frame
        if self.status == "import":
            self.importFrame.place_forget()
        elif self.status == "read":
            self.readFrame.place_forget()
        elif self.status == "select":
            self.selectFrame.place_forget()
        #place the new frame
        if(method == "import"):
            self.importFrame.place(width=self.canvas_width, height=self.canvas_height)
        elif(method == "select"):
            self.selectFrame.place(width=self.canvas_width, height=self.canvas_height)
        elif(method == "read"):
            self.readFrame.place(width=self.canvas_width, height=self.canvas_height)

        # self.content.width = self.canvas_width
        # self.content.height = self.canvas_height
        # self.content.grid(row=0, column=1, columnspan=4)
        self.status = method

    def setupImport(self):
        self.importFrame = Frame(self.content, width=self.canvas_width, height=self.canvas_height)
        self.header = Label(self.importFrame, text="Import")
        self.header.pack()
        self.title = Label(self.importFrame, text="Title")
        self.title.pack()
        self.titleEntry = Entry(self.importFrame, bd=5)
        self.titleEntry.pack(fill=X)
        self.textLabel = Label(self.importFrame, text="Text")
        self.textLabel.pack()
        # make the entry frame
        self.textEntryFrame = Frame(self.importFrame)
        self.textEntryScrollbar = Scrollbar(self.textEntryFrame)
        self.textEntry = Text(self.textEntryFrame, yscrollcommand=self.textEntryScrollbar.set)
        self.textEntry.pack(side=LEFT, fill=BOTH, expand=1)
        self.textEntryScrollbar.pack(side=RIGHT, fill=Y)
        self.textEntryScrollbar.config(command=self.textEntry.yview)
        self.textEntryFrame.pack(fill=BOTH, expand=1)
        # end the entry frame
        self.add = Button(self.importFrame, text="Add to Library", command=lambda: self.contentListener("add"))
        self.add.pack()
        self.statusLabel = Label(self.importFrame)
        self.statusLabel.pack()

    def setupRead(self):
        self.readFrame = Frame(self.content, width=self.canvas_width, height=self.canvas_height)
        self.header = Label(self.readFrame, text="Read")
        self.header.pack()
        self.title = Label(self.readFrame, text="Title")
        self.title.pack()
        self.contentFrame = Frame(self.readFrame)
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

    def setupSelect(self):
        self.selectFrame = Frame(self.content, width=self.canvas_width, height=self.canvas_height)
        self.header = Label(self.selectFrame, text="Make A Selection")
        self.header.pack()
        # make the selection container frame
        self.selectionContainerFrame = Frame(self.selectFrame)
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

    def contentListener(self, action):
        if(action == "add"):
            self.lib.addArticle(Article(self.titleEntry.get(), self.textEntry.get(1.0, END)))
            self.selections.insert(END, self.titleEntry.get())
            self.statusLabel.config(text='Success')
            self.titleEntry.delete(0, END)
            self.textEntry.delete(1.0, END)

    #create a listener for the ListBox
    def onselect(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        # print("Selected article with the title: " + value)
        self.update("read")
        article = self.lib.getArticle(value)
        self.title.config(text=article.getTitle())
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)
        self.text.insert(1.0, article.getTitle() + "\n\n", "title")
        self.text.insert(END, article.getText(), "text")
        self.text.config(state=DISABLED)
        # self.text.tag_add("all", 1.0, END)
        index = 1.0
        lastChar = self.text.index("%s-1c" % END)
        while(index != lastChar):
            character = self.text.get(index)
            if isMeaningfulCharacter(character) is True:
                self.text.tag_add("all", index, "%swordend" % index)
                index = self.text.index("%swordend" % index)
            index = self.text.index("%s+1c" % index)

    #create a listener for the readable text
    def textClickHandler(self, evt):
        # get the index of the mouse click
        index = evt.widget.index("@%s,%s" % (evt.x, evt.y))
        startOfWord = "%swordstart" % index
        endOfWord = "%swordend" % index
        word = self.text.get(startOfWord, endOfWord)
        translations = getTranslation(word, "de", "en")
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


root = Tk()
my_gui = GUI(root)
root.mainloop()
