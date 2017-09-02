from Tkinter import *
from library import Library
from globals import *
from panels import *


class GUI(object):
    def __init__(self, master):
        self.master = master
        master.title("Minerva")

        master.option_add("*Font", "Helvetica 14")

        self.canvas_width = self.master.winfo_screenwidth() - 200
        self.canvas_height = self.master.winfo_screenheight() - 200

        self.menu = Frame(master)
        self.menu.grid(row=0, column=0)

        self.content = Frame(master, width=self.canvas_width, height=self.canvas_height)
        self.content.grid(row=0, column=1, columnspan=4)

        self.setUpDirectories()

        #Setup the menu bar
        self.menuLabel = Label(self.menu, text="Menu")
        self.menuLabel.pack()
        self.importButton = Button(self.menu, text="Import", command=lambda: self.update("import"))
        self.importButton.pack()
        self.readButton = Button(self.menu, text="Read", command=lambda: self.update("select"))
        self.readButton.pack()
        self.saveButton = Button(self.menu, text="Save", command=lambda: self.update("save"))
        self.saveButton.pack()
        self.statsButton = Button(self.menu, text="Stats", command=lambda: self.update("stats"))
        self.statsButton.pack()

        #Setup the possible content pages
        self.importPanel = ImportPanel(self.content, self)
        self.readPanel = ReadPanel(self.content, self)
        self.selectPanel = SelectPanel(self.content, self)
        self.statsPanel = StatsPanel(self.content, self)

        # default to the import page
        self.status = "import"
        self.update("import")

        self.lib = Library()

        # Add the window close listener for automatic saving
        master.protocol("WM_DELETE_WINDOW", self.closeActions)

    def update(self, method):
        if method == "save":
            self.readPanel.saveWordLists()
        else:
            #remove the old panel
            if self.status == "import":
                self.importPanel.getFrame().place_forget()
            elif self.status == "read":
                self.readPanel.saveWordLists()
                self.readPanel.getFrame().place_forget()
            elif self.status == "select":
                self.selectPanel.getFrame().place_forget()
            elif self.status == "stats":
                self.statsPanel.getFrame().place_forget()
            #place the new panel
            if(method == "import"):
                self.importPanel.getFrame().place(width=self.canvas_width, height=self.canvas_height)
            elif(method == "select"):
                self.selectPanel.getFrame().place(width=self.canvas_width, height=self.canvas_height)
            elif(method == "read"):
                self.readPanel.getFrame().place(width=self.canvas_width, height=self.canvas_height)
            elif(method == "stats"):
                self.statsPanel.getFrame().place(width=self.canvas_width, height=self.canvas_height)

            self.status = method

    def importArticle(self, article):
        self.lib.addArticle(article)
        self.selectPanel.addSelection(article.getTitle())

    def articleSelected(self, articleTitle):
        self.update("read")
        article = self.lib.getArticle(articleTitle)
        self.readPanel.displayArticle(article)

    def closeActions(self):
        self.readPanel.saveWordLists()
        self.master.destroy()

    def setUpDirectories(self):
        try:
            os.makedirs(rootDirectory)
        except OSError:
            if not os.path.isdir(rootDirectory):
                raise
        try:
            os.makedirs(artFolderName)
        except OSError:
            if not os.path.isdir(artFolderName):
                raise
        try:
            os.makedirs(wlFolderName)
        except OSError:
            if not os.path.isdir(wlFolderName):
                raise

root = Tk()
my_gui = GUI(root)
root.mainloop()
