import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import os
import csv
import copy
import statistics

os.chdir(os.path.dirname(os.path.realpath(__file__)))

colnames = []
select_nor = ["0,1", "1,10", "0,10", "-1,1", "Z-Scores"]
props = ["high good", "low good", "descriptive"]
#io = ["input", "output"]
colchoices = []
col_io_choices = []
col_input_choices = []
col_output_choices = []
colprops = {}
col_io = {}
col_inputs = {}
col_outputs = {}
oldList = False
inputbox = tk.Listbox
outputbox = tk.Listbox


class CSVReader(tk.Frame):
     def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        def NormalizeData(pin):
            type = normal_opts.get()
            # Create copy of the CSV file
            data_Normalized = copy.deepcopy(data)

            for x in range(len(data[1])):
                row_count = 1

            #region Details/Examples
            # This is used to check if the item in the column is numeric
            # It looks at the sting value stored there at checks the last character in the string
            # Example: 1.234 | Checks '4' and then assumes the column is numeric
            # Example: Arizona Cardinals | Checks 's' and then assumes the column is non-numeric
            #endregion
                size = len(data[1][x])
                if data[1][x][size - 1].isdigit():

                #region Loop/Math
                # List is created that holds all the data in the column
                # Removes the first index since that is the headers
                # Converts list into integers before sorting
                # Loops while there is still a row in data and fills it in with Normalized Data
                # Breaks when it is at the final row of the CSV file
                # endregion 
                    temp_col = [sub[x] for sub in data]
                    temp_col.pop(0)
                    temp_col = list(map(float, temp_col))
                    temp_col.sort()

                    stdv_temp_col = statistics.stdev(temp_col)

                    if pin != "pin":
                        while row_count != len(data):
                            if type == "0,1":
                                data_Normalized[row_count][x] = f'{(float(data[row_count][x]) - min(temp_col)) / (max(temp_col) - min(temp_col)):.4f}'
                            elif type == "1,10":
                                data_Normalized[row_count][x] = f'{1 + (float(data[row_count][x]) - min(temp_col)) / (max(temp_col) - min(temp_col)) * 9:.4f}'
                            elif type == "0,10":
                                data_Normalized[row_count][x] = f'{(float(data[row_count][x]) - min(temp_col)) / (max(temp_col) - min(temp_col)) * 10:.4f}'
                            elif type == "-1,1":
                                data_Normalized[row_count][x] = f'{(float(data[row_count][x]) - min(temp_col)) / (max(temp_col) - min(temp_col)) * 2 - 1:.4f}'
                            elif type == "Z-Scores":
                                data_Normalized[row_count][x] = f'{(float(data[row_count][x]) - statistics.mean(temp_col)) / (stdv_temp_col):.4f}'
                            else:
                                pass
                            row_count += 1
                    else:
                        pass

            norm_delete_command()
            data_Normalized.pop(0)

            for colindex, col in enumerate(colnames):
                self.tree.heading("#" + str(colindex + 1), text=col, command=expand)   
            for row in data_Normalized:
                self.tree.insert("", "end", values=row)


        def expand():
            newRoot = tk.Tk()

        def reset():
            normal_opts.set("----")
            NormalizeData("")
        
        def ColumnOpts():
            global colprops
            global col_io
            global col_io_choices
            global col_input_choices
            global col_output_choices
            global colnames
            global colchoices
            global oldList
            i=0

            newWindow = Toplevel(self)

            newWindow.title("New Window")
    
            newWindow.geometry("1500x500")

            if len(colchoices) != 0 or len(col_io_choices) == 0:
                oldList = True

            Label(newWindow, text = "Specify Column Properties", font="Helvetica 18 bold").grid(row=1, column=2, sticky=N )

            Label (newWindow, text= "Data Context (Lower/Higher the better)").grid(row = 2, column = 2, ipadx=10)
            Label (newWindow, text= "Inputs (What Impacts this Column?)").grid(row = 2, column = 3, ipadx=10)
            Label (newWindow, text= "Outputs (What Columns are Impacted?)").grid(row = 2, column = 4, ipadx=10)

            if oldList == True:
                    colchoices = []
                    col_io_choices = []
                    col_input_choices = []
                    col_output_choices = []

            while i < len(colnames):

                OPTIONS = props
                #OPTIONS2 = colnames
                #OPTIONS3 = colnames
                variable = tk.StringVar(value="Choose High/Low")
                #variable2 = tk.StringVar(value="Choose Inputs")
                #variable3 = tk.StringVar(value="Choose Outputs")
                optionname = Label(newWindow, text = str(colnames[i]))

                if len(colchoices) != len(colnames):    
                    colchoices.append(variable)
                #if len(col_input_choices) != len(colnames):
                    #col_input_choices.append(variable2)
                #if len(col_output_choices) != len(colnames):
                    #col_output_choices.append(variable3)

                dropdown = OptionMenu( newWindow, variable,  *OPTIONS)
                inputbutton = tk.Button(newWindow, text="Choose Inputs (What effects this column?)", padx= '20', command= lambda c=i: inputbox(c))
                outputbutton = tk.Button(newWindow, text="Choose Outputs (What is effected by this column?)", padx= '20', command= lambda c=i: outputbox(c))
                #dropdown2 = OptionMenu ( newWindow, variable2, *OPTIONS2)
                #dropdown3 = OptionMenu( newWindow, variable3, *OPTIONS3)
                optionname.grid(row=i+4, column = 1)
                dropdown.grid(row=i+4, column=2, ipadx = 30, ipady = 5)
                inputbutton.grid(row=i+4, column=3, ipadx = 30, ipady = 5)
                outputbutton.grid(row= i+4, column = 4, ipadx= 30, ipady= 5)



                i = i+1

            confirm = tk.Button(newWindow, text='Confirm', command=returnVars)
            confirm.grid(row = len(colnames) + 4, column=2, ipadx= 10, ipady= 5)


        def clear_frame():
            for widgets in self.winfo_children():
                print(widgets.widgetName)
                if widgets.widgetName == "toplevel":
                    widgets.destroy()  

        def returnVars():
            clear_frame()
            Current = Toplevel(self)


            for num, var in enumerate(colchoices):
                if var.get() != "" and var.get() != "Choose High/Low":
                    colprops[colnames[num]] = var.get()

            #for num2, var2 in enumerate(col_input_choices):
             #   if colprops[colnames[num2]] != "descriptive":
              #      col_inputs[colnames[num2]].append(var2)

#            for num3, var3 in enumerate(col_output_choices):
 #               if var3 != "" and var3 != "Choose Outputs" and colprops[colnames[num3]] != "descriptive":
  #                  col_outputs[colnames[num3]].append(var3)

            Label (Current, text= "Current Settings", font="Helvetica 16 bold").grid(row=0, column=1)
            Label (Current, text= "Data Context (Lower/Higher the better)").grid(row = 0, column = 2, ipadx=10)
            Label (Current, text= "Data Inputs ").grid(row = 0, column = 3, ipadx=10)
            Label (Current, text= "Data Outputs ").grid(row = 0, column = 4, ipadx=10)
            for i, colprop in enumerate(colprops):
                Label(Current, text= colprop + " :").grid(row = i+1, column = 1, ipadx=10)
                Label(Current, text = str(colprops[colnames[i]]), font="bold").grid(row = i+1, column=2)
                if colprops[colnames[i]] == "descriptive":
                    Label(Current, text = "N/A", font="bold").grid(row = i+1, column=3)
                    col_inputs[colnames[i]] = "N/A"
                    Label(Current, text = "N/A", font="bold").grid(row = i+1, column=4)
                    col_outputs[colnames[i]] = "N/A"

                elif col_inputs[colnames[i]] == []:
                    Label(Current, text = "None", font="bold").grid(row = i+1, column=3)
                else:
                    Label(Current, text = str(col_inputs[colnames[i]]), font="bold").grid(row = i+1, column=3)

                if col_outputs[colnames[i]] == []:
                    Label(Current, text = "None", font="bold").grid(row = i+1, column=4)
                else:
                    Label(Current, text = str(col_outputs[colnames[i]]), font="bold").grid(row = i+1, column=4)



        def inputbox(index):
            global colnames
            global inputbox
            Current = Toplevel(self)
            Current.title(str(colnames[index]) + " Input Settings")
            inputvar = tk.Variable(value=colnames)

            inputbox = tk.Listbox(
            Current,
            listvariable=inputvar,
            height=30,
            width=100,
            selectmode=tk.EXTENDED
            )

            inputbox.pack(expand=True, fill=tk.BOTH)
            bind_input_button = tk.Button(Current, text="Confirm", padx= '20', command= lambda: input_items_selected(index))
            bind_input_button.pack(side=tk.BOTTOM)

        def input_items_selected(index):
            global inputbox
            global colnames
            global col_inputs
            selectedindices = inputbox.curselection()
            choices_temp = [inputbox.get(i) for i in selectedindices]
            col_inputs[colnames[index]] = choices_temp
            

        def outputbox(index):
            global outputbox
            global colnames
            global col_output_choices
            Current = Toplevel(self)
            Current.title(str(colnames[index]) + " Output Settings")
            outputvar = tk.Variable(value=colnames)

            outputbox = tk.Listbox(
            Current,
            listvariable=outputvar,
            height=20,
            width=100,
            selectmode=tk.EXTENDED
            )

            outputbox.pack(expand=True, fill=tk.BOTH)
            bind_output_button = tk.Button(Current, text="Confirm", padx= '20', command= lambda: output_items_selected(index))
            bind_output_button.pack(side=tk.BOTTOM)

        def output_items_selected(index):
            global outputbox
            global colnames
            global col_outputs
            selectedindices = outputbox.curselection()
            choices_temp = [outputbox.get(i) for i in selectedindices]
            col_outputs[colnames[index]] = choices_temp

        def UploadAction(event=None):
                delete_command()
                global colnames
                global data
                global colprops
                global col_io
                global col_inputs
                global col_outputs

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
                    
                    if len(col_inputs) == 0:
                        col_inputs = {colname: [] for colname in colnames}

                    if len(col_outputs) == 0:
                        col_outputs = {colname: [] for colname in colnames}

                    for colindex, col in enumerate(colnames):
                        self.tree.heading("#" + str(colindex + 1), text=col)   


                    for row in csv_reader:
                        self.tree.insert("", "end", values=row)
                with open(filename) as csv_file:
                    data = list(csv.reader(csv_file, delimiter=','))

        def norm_delete_command():
            for col in self.tree['columns']:
                self.tree.heading(col, text='')
            self.tree.delete(*self.tree.get_children())

        def delete_command():
            global colprops
            global oldList
            global col_io
            global col_inputs
            global col_outputs
            global colnames
            colnames = []
            for col in self.tree['columns']:
                self.tree.heading(col, text='')
            self.tree.delete(*self.tree.get_children())
            oldList = False
            colprops = {}
            col_io = {}
            col_inputs = {}
            col_outputs = {}


        self.topFrame = tk.Frame(self, bg="darkred", pady="10", padx="10", 
                            width="200", height="50")     
        self.topFrame.pack(side=tk.TOP)   
        self.topFrame.pack_propagate(0)
        
        self.headerLabel = tk.Label(self.topFrame, text=" Upload CSV ", 
                            bg="white", fg="navy", font="24")
        self.headerLabel.pack(fill=tk.X)      


        self.middleFrame = tk.Frame(self, bg="white", pady="10", padx="10", 
                            width="200", height="150")

        self.middleFrame.pack()
        self.middleFrame.pack_propagate(0)

        self.button = tk.Button(self.middleFrame, text='Open', padx= '15', command=UploadAction)
        self.button.pack()

        resetButton = tk.Button(self.middleFrame, text="Reset", padx= '20', command=reset, fg='red')
        resetButton.pack(side=tk.BOTTOM)

        normal_opts = tk.StringVar()
        normal_opts.set("----")
        nor_drop = tk.OptionMenu(self.middleFrame, normal_opts, *select_nor)   
        nor_drop.pack(side=tk.BOTTOM, padx= '20')

        normalButton_pin = tk.Button(self.middleFrame, text="Normalize & Pin Outliers", padx= '15', command=lambda: NormalizeData("pin"))
        normalButton_pin.pack(side=tk.BOTTOM)

        normalButton = tk.Button(self.middleFrame, text="Normalize", padx= '20', command=lambda: NormalizeData(""))
        normalButton.pack(side=tk.BOTTOM)

        self.dropFrame = tk.Frame(self, bg="white", pady="10", padx="10", 
                             width = "200", height="50")
        
        self.drop = tk.Button(self.dropFrame, text='Specify Column Properties', command=ColumnOpts)
        self.drop.pack()

        self.dropFrame.pack()
        self.dropFrame.pack_propagate(0)

        self.bottomFrame = ttk.Frame(self)
        self.bottomFrame.pack(expand=tk.YES, fill=tk.BOTH)

    

        self.tree = ttk.Treeview(self.bottomFrame,columns=colnames, show='headings')

        self.scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.scrollbar2 = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand= self.scrollbar.set)
        self.tree.configure(xscrollcommand= self.scrollbar2.set)

                # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.pack(side="bottom", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar2.pack(side="bottom", fill="x")


if __name__ == "__main__":
    root=tk.Tk()
    root.geometry("1500x500")
    root.pack_propagate(0)
    CSVReader(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
