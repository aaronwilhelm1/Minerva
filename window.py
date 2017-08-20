from Tkinter import Tk, Label, Button, Frame, Entry, Text, X, END


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
        self.readButton = Button(self.menu, text="Read", command=lambda: self.update("read"))
        self.readButton.pack()
        self.reviewButton = Button(self.menu, text="Review", command=lambda: self.update("review"))
        self.readButton.pack()
        self.statsButton = Button(self.menu, text="Stats", command=lambda: self.update("stats"))
        self.statsButton.pack()

        #Setup the possible content pages
        self.setupImport()

        #default to the import page
        self.update("import")

    def update(self, method):
        self.status = method
        if(method == "import"):
            self.importFrame.place(width=canvas_width, height=canvas_height)
        else:
            self.importFrame.place_forget()
        self.content.width = canvas_width
        self.content.height = canvas_height
        self.content.grid(row=0, column=1, columnspan=4)

    def setupImport(self):
        self.importFrame = Frame(self.content, width=canvas_width, height=canvas_height)
        self.header = Label(self.importFrame, text="Import")
        self.header.pack()
        self.title = Label(self.importFrame, text="Title")
        self.title.pack()
        self.titleEntry = Entry(self.importFrame, bd=5)
        self.titleEntry.pack()
        self.textLabel = Label(self.importFrame, text="Text")
        self.textLabel.pack()
        self.text = Text(self.importFrame)
        self.text.pack(fill=X)
        self.add = Button(self.importFrame, text="Add to Library", command=lambda: self.contentListener("add"))
        self.add.pack()

    def contentListener(self, action):
        if(action == "add"):
            print(self.titleEntry.get())
            print(self.text.get(1.0, END))


root = Tk()
my_gui = GUI(root)
root.mainloop()
