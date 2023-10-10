import tkinter as tk
from tkinter import filedialog
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))
root = tk.Tk()
root.geometry("400x400")   # size of interface width x height
root.pack_propagate(0)


def UploadAction(event=None):
    descCols = []
    col_names = []
    filename = filedialog.askopenfilename()
    with open(filename, "r") as f:
        for line in f:
            if line.strip():
                x = line.rstrip().split(",") 
                descCols.append(x)
                break
    for cols in descCols:
        for names in cols:
            col_names.append(names)
    for i, col_names in enumerate(col_names, start=1):
        tk.Label(bottomFrame, text = col_names).grid(row=3, column=i, padx=10)
   



# establish three main vertical regions
topFrame = tk.Frame(root, bg="darkred", pady="10", padx="10", 
                    width="400", height="100")     # frame is a container, root is its parent
topFrame.pack(side=tk.TOP)    # pack() helps determine where an item will be placed
topFrame.pack_propagate(0)
# without pack_propagate(0) tkinter sizes things to just the size needed
# with pack_propagate(0) you must set a width and height or they are by default 0

middleFrame = tk.Frame(root, bg="white", pady="10", padx="10", 
                       width="400", height="300")
middleFrame.pack()
middleFrame.pack_propagate(0)


# https://www.tutorialspoint.com/python/tk_label.htm
headerLabel = tk.Label(topFrame, text=" Upload CSV ", 
                       bg="white", fg="navy", font="24")
# bg background color  fg foreground/font color 
headerLabel.pack(fill=tk.X)      # fill container horizontally
# https://www.tutorialspoint.com/python/tk_pack.htm


button = tk.Button(middleFrame, text='Open', command=UploadAction)
button.pack()

bottomFrame = tk.Frame(root, bg="navy", pady="10", padx="10", 
                       width="400", height="225")
bottomFrame.pack()
bottomFrame.pack_propagate(0)

root.mainloop()