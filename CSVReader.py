import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import os
import csv
os.chdir(os.path.dirname(os.path.realpath(__file__)))
colnames = []
props = ["high good", "low good", "descriptive"]
io = ["input", "output"]
colchoices = []
col_io_choices = []
colprops = {}
col_io = {}
oldList = False


class CSVReader(tk.Frame):
     def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

                
        def ColumnOpts():
            global colprops
            global col_io
            global col_io_choices
            global colnames
            global colchoices
            global oldList
            i=0
            
            newWindow = Toplevel(self)
        
            # sets the title of the
            # Toplevel widget
            newWindow.title("New Window")
        
            # sets the geometry of toplevel
            newWindow.geometry("1500x500")
            

            if len(colchoices) != 0 or len(col_io_choices) == 0:
                oldList = True

            Label(newWindow, text = "Specify Column Properties", font="Helvetica 18 bold").grid(row=1, column=2, sticky=N )
            
            Label (newWindow, text= "Data Context (Lower/Higher the better)").grid(row = 2, column = 2, ipadx=10)
            Label (newWindow, text= "Data  IO (Input/Output)").grid(row = 2, column = 3, ipadx=10)

            if oldList == True:
                    colchoices = []
                    col_io_choices = []
            while i < len(colnames):

                OPTIONS = props
                OPTIONS2 = io
                variable = tk.StringVar()
                variable2 = tk.StringVar()
                optionname = Label(newWindow, text = str(colnames[i]))
                #optionname2 = Label(newWindow, text = str(colnames[i]))
                
                if len(colchoices) != len(colnames):    
                    colchoices.append(variable)
                if len(col_io_choices) != len(colnames):
                    col_io_choices.append(variable2)
                
                dropdown = OptionMenu( newWindow, variable,  *OPTIONS)
                dropdown2 = OptionMenu ( newWindow, variable2, *OPTIONS2)
                #dropdown.grid(row=i+2, column= 1)
                optionname.grid(row=i+4, column = 1)
                dropdown.grid(row=i+4, column=2, ipadx = 30, ipady = 5)
                dropdown2.grid(row=i+4, column=3, ipadx = 30, ipady = 5)
                #optionname2.grid
                

                i = i+1

            
                
            ''' Label (newWindow, text= "Data Context (Lower/Higher the better)").grid(row = 2, column = 6, ipadx=10)
                Label (newWindow, text= "Data  IO (Input/Output)").grid(row = 2, column = 7, ipadx=10)
            for i, colprop in enumerate(colprops):
                Label (newWindow, text= "|").grid(row = i+4, column = 4, ipadx=10)
                Label(newWindow, text= colprop + " :").grid(row = i+4, column = 5, ipadx=10)
                Label(newWindow, text = str(colprops[colnames[i]])).grid(row = i+4, column=6)
                Label(newWindow, text = str(col_io[colnames[i]])).grid(row = i+4, column=7)'''
            
            confirm = tk.Button(newWindow, text='Confirm', command=returnVars)
            confirm.grid(row = len(colnames) + 4, column=2, ipadx= 10, ipady= 5)
            #scrollbarCols = ttk.Scrollbar(newWindow, orient="vertical", command=)
            #scrollbarCols.grid(side="right", fill="y")
            
         
        def clear_frame():
            for widgets in self.winfo_children():
                if widgets.widgetName == "toplevel":
                    widgets.destroy()  

        def returnVars():
            clear_frame()
            Current = Toplevel(self)
            
            for cols in colchoices :
                print(cols.get())
            for num, var in enumerate(colchoices):
                if var.get() != "":
                    colprops[colnames[num]] = var.get()
            
            for num2, var2 in enumerate(col_io_choices):
                if var2.get() != "":
                    col_io[colnames[num2]] = var2.get()
            Label (Current, text= "Current Settings", font="Helvetica 16 bold").grid(row=0, column=1)
            Label (Current, text= "Data Context (Lower/Higher the better)").grid(row = 0, column = 2, ipadx=10)
            Label (Current, text= "Data  IO (Input/Output)").grid(row = 0, column = 3, ipadx=10)
            for i, colprop in enumerate(colprops):
                Label(Current, text= colprop + " :").grid(row = i+1, column = 1, ipadx=10)
                Label(Current, text = str(colprops[colnames[i]])).grid(row = i+1, column=2)
                Label(Current, text = str(col_io[colnames[i]])).grid(row = i+1, column=3)
            


                
        
        def UploadAction(event=None):
                delete_command()
                global colnames
                global colprops
                global col_io
                colnames = []
                filename = filedialog.askopenfilename()
                # Open and read the CSV file
                with open(filename, "r") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    
                    for row in csv_reader:
                        for element in row:
                            colnames.append(element)
                        self.tree.configure(columns=colnames)    
                        break
                    if len(colprops) == 0:
                        colprops = {colname: None for colname in colnames}
                    if len(col_io) == 0:
                        col_io = {colname: None for colname in colnames}
         
                    for colindex, col in enumerate(colnames):
                        self.tree.heading("#" + str(colindex + 1), text=col)   


                    for row in csv_reader:
                        self.tree.insert("", "end", values=row)
        
        def delete_command():
            global colprops
            global col_io
            


            for col in self.tree['columns']:
                self.tree.heading(col, text='')
            self.tree.delete(*self.tree.get_children())
            colprops = {}
            col_io = {}
        self.topFrame = tk.Frame(self, bg="darkred", pady="10", padx="10", 
                            width="200", height="50")     
        self.topFrame.pack(side=tk.TOP)   
        self.topFrame.pack_propagate(0)


        
        self.headerLabel = tk.Label(self.topFrame, text=" Upload CSV ", 
                            bg="white", fg="navy", font="24")
        self.headerLabel.pack(fill=tk.X)      


        self.middleFrame = tk.Frame(self, bg="black", pady="10", padx="10", 
                            width="200", height="100")

        self.middleFrame.pack()
        self.middleFrame.pack_propagate(0)

        self.dropFrame = tk.Frame(self, bg="white", pady="10", padx="10", 
                             width = "200", height="50")
        self.dropFrame.pack()
        self.dropFrame.pack_propagate(0)


        self.drop = tk.Button(self.dropFrame, text='Specify Column Properties', command=ColumnOpts)
        self.drop.pack()
        self.button = tk.Button(self.middleFrame, text='Open', command=UploadAction)
        self.button.pack()

        self.bottomFrame = ttk.Frame(self)
        self.bottomFrame.pack(expand=tk.YES, fill=tk.BOTH)


        self.tree = ttk.Treeview(self.bottomFrame,columns=colnames, show='headings')

        self.scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.scrollbar2 = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand= self.scrollbar.set)
        self.tree.configure(xscrollcommand= self.scrollbar2.set)

                # Pack the Treeview and scrollbar
        self.tree.pack(side="bottom", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar2.pack(side="bottom", fill="x")


if __name__ == "__main__":
    root=tk.Tk()
    root.geometry("1500x500")
    root.pack_propagate(0)
    CSVReader(root).pack(side="top", fill="both", expand=True)
    root.mainloop()