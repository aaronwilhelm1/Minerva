from Tkinter import Tk, Label, Button, Frame


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

    def update(self, method):
        #TODO
        print("A Button was pushed")

root = Tk()
my_gui = GUI(root)
root.mainloop()
