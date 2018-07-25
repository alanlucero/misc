from tkinter import *
import tkinter.messagebox
import datetime, time

def doNothing():
    print("Doing nothing")

# **** Message for verification*****
def verification():
    verification = tkinter.messagebox.askquestion("Verification of order details","Have you verified that all details provided are correct?")
    ts = time.time()
    ts_str = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S %Y-%m-%d ')
    if verification == 'yes':
        text = 'Order verified and sent at ' + ts_str
        comms.config(text=text)
    else:
        text = 'Order cancelled at ' + ts_str
        comms.config(text=text, fg="red")


root = Tk()
root.configure(background="black")
root.minsize(450,350)

#*******Menu creation*********
menu = Menu(root)
root.config(menu = menu)

#File Menu
subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New Project...", command=doNothing)
subMenu.add_command(label="New...", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=doNothing)

#Edit menu
editMenu = Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Redo", command=doNothing)

# *** Status ***
status = Frame(root, bg="Orange")
status.pack(side=TOP, fill=X)
comms_title = Label(status, text="Status: ", bg="Orange",fg="Black", font= "Helvetica 12 bold")
comms_title.pack(side=LEFT)
comms = Label(status, text="OK", bg="Orange",fg="green", font= "Helvetica 12 bold", bd=1)
comms.pack(side=LEFT)

# ******** Toolbar*****
toolbar = Frame(root, bg="Orange")
toolbar.pack(side=BOTTOM, fill=X)
insert = Button(toolbar, text = "Insert Order",command=verification ,bg="black", fg="white", font= "Helvetica 12 bold")
insert.pack(side=RIGHT, padx = 2, pady = 2)


root.mainloop()





# class windowControls:
#     def __init__(self, master):
#         frame = Frame(master)
#         frame.pack()
#
#         self.printButton = Button(frame, text="Print Message", command=self.printMessage)
#         self.printButton.pack(side=LEFT)
#
#         self.quitButton = Button(frame, text="Quit", command=frame.quit)
#         self.quitButton.pack(side=LEFT)
#
#     def printMessage(self):
#         print("Hello World!")
#
# root = Tk()
# b = windowControls(root)
# root.mainloop()
#




#
# root = Tk()
#
# def helloWorld(event):
#     print("Hello World!")
#
# def byeWorld(event):
#     print("Goodbye World!")
#
# frame = Frame(root,width=300,height=250)
# button1 = Button(root, text="Say Hello")
# button1.bind("<Button-1>",helloWorld)
# button1.bind("<Button-3>",byeWorld)
# button1.grid(row=0,column=1)
#
#
#
# root.mainloop()

# root = Tk()
# root.configure(background="black")
# root.title("Instrument Search for Repo | Cash Management")
# root.minsize(360,350)
#
# #Labels
# label1 = Label(root, bg="black", fg="Orange", text="Name ", font= "Helvetica 14 bold")
# label2 = Label(root, text="Password ", bg="black", fg="Orange", font= "Helvetica 14 bold")
#
# # Entries
# entry1 = Entry(root, fg="black", font= "Helvetica 14 bold")
# entry2 = Entry(root, fg="black", font= "Helvetica 14 bold")
#
# #Grids
# label1.grid(row=0, column=0, sticky=E)
# label2.grid(row=1, column=0, sticky=E)
#
# entry1.grid(row=0, column=1)
# entry2.grid(row=1, column=1)
#
# #checkbox
# c = Checkbutton(root, text="Remember my credentials", bg="black",fg="white")
# c.grid(columnspan=2, sticky=E)
#
#
# root.mainloop()


# one = Label(root,text="One!!!!",bg="red",fg="white")
# one.pack()
# two = Label(root,text="One!!!!",bg="blue",fg="orange")
# two.pack(side = LEFT, fill=X)

# topFrame = Frame(root)
# topFrame.pack()
#
# bottomFrame = Frame(root)
# bottomFrame.pack(side=BOTTOM)
#
# button1 = Button(topFrame, text="Submit", fg="red")
# button2 = Button(topFrame, text="Submit", fg="green")
# button3 = Button(bottomFrame, text="Submit", fg="yellow")
# button4 = Button(bottomFrame, text="Submit", fg="blue")
#
# button1.pack(side = LEFT)
# button2.pack(side = LEFT)
# button3.pack(side = LEFT)
# button4.pack(side = LEFT)

