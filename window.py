from Tkinter import Tk, Label, Button, Frame, Entry, Text, X, END, Listbox, SINGLE, NORMAL, DISABLED, Scrollbar, RIGHT, Y, BOTH, LEFT
from library import Library
from article import Article
from os import listdir
from os.path import isfile, join, splitext
from globals import artFolderName, artFileEnding


canvas_width = 700
canvas_height = 700
debug = True


class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Minerva")

        self.menu = Frame(master)
        self.menu.grid(row=0, column=0)

        self.content = Frame(master, width=canvas_width, height=canvas_height)
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
            self.importFrame.place(width=canvas_width, height=canvas_height)
        elif(method == "select"):
            self.selectFrame.place(width=canvas_width, height=canvas_height)
        elif(method == "read"):
            self.readFrame.place(width=canvas_width, height=canvas_height)

        self.content.width = canvas_width
        self.content.height = canvas_height
        self.content.grid(row=0, column=1, columnspan=4)
        self.status = method

    def setupImport(self):
        self.importFrame = Frame(self.content, width=canvas_width, height=canvas_height)
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
        self.readFrame = Frame(self.content, width=canvas_width, height=canvas_height)
        self.header = Label(self.readFrame, text="Read")
        self.header.pack()
        self.title = Label(self.readFrame, text="Title")
        self.title.pack()
        # make the text frame
        self.textFrame = Frame(self.readFrame)
        self.textScrollbar = Scrollbar(self.textFrame)
        self.text = Text(self.textFrame, state=DISABLED, yscrollcommand=self.textScrollbar.set)
        # self.text.pack(fill=X)
        self.text.pack(side=LEFT, fill=Y)
        self.textScrollbar.pack(side=RIGHT, fill=Y)
        self.textScrollbar.config(command=self.text.yview)
        self.textFrame.pack(fill=BOTH, expand=1)
        #end the text frame

    def setupSelect(self):
        self.selectFrame = Frame(self.content, width=canvas_width, height=canvas_height)
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
        self.text.insert(1.0, article.getText())
        self.text.config(state=DISABLED)


root = Tk()
my_gui = GUI(root)
root.mainloop()
