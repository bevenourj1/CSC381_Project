import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import os
import csv
import copy
import statistics
import matplotlib.pyplot as plt
import re

os.chdir(os.path.dirname(os.path.realpath(__file__)))

colnames = []
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

        # Create a method to sort columns
        def sort_column(col_index, reverse):
            data = [(float(self.tree.set(child, col_index)), child) for child in self.tree.get_children('')]
            data.sort(reverse=reverse)
            for i, item in enumerate(data):
                self.tree.move(item[1], '', i)
            self.tree.heading(col_index, command=lambda: sort_column(col_index, not reverse))

        def reset():
            self.tree.delete(*self.tree.get_children())
            for colindex, col in enumerate(colnames):
                self.tree.heading("#" + str(colindex + 1), text=str(colindex) + str('. ') + col)   
            for row in data:
                if row == colnames:
                    pass
                else:
                    self.tree.insert("", "end", values=row)
        
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
                        self.tree.heading("#" + str(colindex + 1), text=str(colindex) + str('. ') + col)  


                    for row in csv_reader:
                        self.tree.insert("", "end", values=row)
                with open(filename) as csv_file:
                    data = list(csv.reader(csv_file, delimiter=','))

        # Sort Window
        def open_sort_window():
            sort_window = tk.Tk()
            sort_window.title("Sort Options")

            def set_col_num():
                global col_num
                col_num = int(entry.get())

            label = tk.Label(sort_window, text="Enter the column number to sort:")
            label.pack()

            # Column number input
            entry = tk.Entry(sort_window)
            entry.pack()

            # the "Descending" button
            sort_desc_button = tk.Button(sort_window, text="Descending", command=lambda: (set_col_num(), sort_column(colnames[col_num], True)))
            sort_desc_button.pack(side=tk.BOTTOM)

            # the "Ascending" button
            sort_button = tk.Button(sort_window, text="Ascending", command=lambda: (set_col_num(), sort_column(colnames[col_num], False)))
            sort_button.pack(side=tk.BOTTOM)

            sort_window.mainloop()

        # Scatter PLot Window
        def scatter_plot_window():
            sp_window = tk.Tk()
            sp_window.title("Scatter Plot")
            sp_window.geometry("360x100")

            # Set columns 1 & 2 for the scatter plot
            def set_scatter_plot():
                global col1, col2
                col1_input = entry1.get()
                col2_input = entry2.get()

                # Validate the user input
                if not col1_input.isdigit() or not col2_input.isdigit():
                    messagebox.showerror("Error", "Please enter valid column numbers as integers.")
                    return

                col1 = int(col1_input)
                col2 = int(col2_input)

                # Check if the column numbers are within the valid range
                if col1 < 0 or col1 >= len(colnames) or col2 < 0 or col2 >= len(colnames):
                    messagebox.showerror("Error", "Column numbers are out of range.")
                    return
                
                scatter_plot()

            label = tk.Label(sp_window, text="Enter the column numbers:")
            label.pack()

            entry1 = tk.Entry(sp_window)
            entry1.pack(side=tk.LEFT)
            
            entry2 = tk.Entry(sp_window)
            entry2.pack(side=tk.RIGHT)

            create_sp_button = tk.Button(sp_window, text="Create Scatter Plot", command=set_scatter_plot)
            create_sp_button.pack(side=tk.BOTTOM)

        # Create the Scatter Plot
        def scatter_plot():
            if col1 is not None and col2 is not None:
                x = []
                y = []
                for row in data[1:]:
                    try:
                        x_value = float(row[col1])
                        y_value = float(row[col2])
                        x.append(x_value)
                        y.append(y_value)
                    except ValueError:
                        pass

                plt.figure()
                plt.scatter(x, y, marker='o', alpha=0.5)
                plt.xlabel(colnames[col1])
                plt.ylabel(colnames[col2])
                plt.title(f"Scatter Plot: {colnames[col1]} vs {colnames[col2]}")
                plt.show()

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

        button_width = 20

        self.button = tk.Button(self.middleFrame, text='Open', padx= '15', command=UploadAction)
        self.button.pack()

        resetButton = tk.Button(self.middleFrame, text="Reset", padx= '20', command=reset, fg='red')
        resetButton.pack(side=tk.BOTTOM)

        # Create the "Scatter Plot" button
        sp_button = tk.Button(self.middleFrame, text="Scatter Plot", width=button_width, command=scatter_plot_window)
        sp_button.pack(side=tk.BOTTOM)

        normalButton_pin = tk.Button(self.middleFrame, text=" Normalize Data ", width= 20, command=lambda: norm_error())
        normalButton_pin.pack(side=tk.BOTTOM)

        # Create the "Sort" button
        sort_button = tk.Button(self.middleFrame, text="Sort", width=button_width, command=open_sort_window)
        sort_button.pack(side=tk.BOTTOM)

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

def norm_error():
    try:
        NormalizationWindow(data)
    except NameError:
        messagebox.showerror(" No File ", " Please select a CSV file first ")
    
def NormalizeData(pin, norm_type, data, norm_tree):  

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
            mean_temp_col = statistics.mean(temp_col)

            while row_count != len(data):

                if norm_type == " 0, 1 ":
                    if pin.get() == "(Pinned)" and float(data[row_count][x]) > (stdv_temp_col * 3 + mean_temp_col):
                        data_Normalized[row_count][x] = '(1)'
                    elif pin.get() == "(Pinned)" and float(data[row_count][x]) < (mean_temp_col - (stdv_temp_col * 3)):
                        data_Normalized[row_count][x] = '(0)'
                    else:
                        data_Normalized[row_count][x] = f'{(float(data[row_count][x]) - min(temp_col)) / (max(temp_col) - min(temp_col)):.4f}'

                elif norm_type == " 1, 10 ":
                    if pin.get() == "(Pinned)" and float(data[row_count][x]) > ((stdv_temp_col * 3) + mean_temp_col):
                        data_Normalized[row_count][x] = '(10)'

                        print("\nRow: " + str(data[row_count][0]) + " | Column: " + str(data[0][x] + " was pinned(H)!"))
                        print("The Value was: " + str(data[row_count][x]))
                        print("The Mean plus the Dev * 3 was: " + str((mean_temp_col + (stdv_temp_col * 3))))
                        

                    elif pin.get() == "(Pinned)" and float(data[row_count][x]) < (mean_temp_col - (stdv_temp_col * 3)):
                        data_Normalized[row_count][x] = '(1)'

                        print("\nRow: " + str(data[row_count][x]) + " | Column: " + str(data[0][x] + " was pinned(L)!"))
                        print("The Mean minus the Dev * 3 was: " + str((mean_temp_col - (stdv_temp_col * 3))))
                        print("The Value was: " + str(data[row_count][x]))

                    else:
                        data_Normalized[row_count][x] = f'{1 + (float(data[row_count][x]) - min(temp_col)) / (max(temp_col) - min(temp_col)) * 9:.4f}'

                elif norm_type == " 0, 10 ":
                    if pin.get() == "(Pinned)" and float(data[row_count][x]) > ((stdv_temp_col * 3) + mean_temp_col):
                        data_Normalized[row_count][x] = '(10)'
                    elif pin.get() == "(Pinned)" and float(data[row_count][x]) < (mean_temp_col - (stdv_temp_col * 3)):
                        data_Normalized[row_count][x] = '(0)'
                    else:
                        data_Normalized[row_count][x] = f'{(float(data[row_count][x]) - min(temp_col)) / (max(temp_col) - min(temp_col)) * 10:.4f}'

                elif norm_type == " -1, 1 ":
                    if pin.get() == "(Pinned)" and float(data[row_count][x]) > ((stdv_temp_col * 3) + mean_temp_col):
                        data_Normalized[row_count][x] = '(1)'
                    elif pin.get() == "(Pinned)" and float(data[row_count][x]) < (mean_temp_col - (stdv_temp_col * 3)):
                        data_Normalized[row_count][x] = '(-1)'
                    else:
                        data_Normalized[row_count][x] = f'{(float(data[row_count][x]) - min(temp_col)) / (max(temp_col) - min(temp_col)) * 2 - 1:.4f}'

                elif norm_type == " Z-Scores ":
                    if pin.get() == "(Pinned)":
                        pin.set('')
                        data_Normalized[row_count][x] = f'{(float(data[row_count][x]) - (mean_temp_col)) / (stdv_temp_col):.4f}'
                    else:
                        data_Normalized[row_count][x] = f'{(float(data[row_count][x]) - (mean_temp_col)) / (stdv_temp_col):.4f}'
                else:
                    pass

                row_count += 1

    for colindex, col in enumerate(colnames):
        norm_tree.heading("#" + str(colindex + 1), text=col)   
    for row in data_Normalized:
        if row == colnames:
            pass
        else:
            norm_tree.insert("", "end", values=row)    

def TopNCal(nTree, normTree, n, type):
    nTree.delete(*nTree.get_children())

    nDict = {}

    for col in nTree['columns']:
        nTree.column(col, width=10)
        nTree.heading(col, text=col) 
    
    rowCheck = 0 
    for item in normTree.get_children():
        values = normTree.item(item,'values')
        rowValue = 0

        for item in values:
            item = re.sub(r'\(', '', item)
            item = re.sub(r'\)', '', item)

            try:
                rowValue += float(item)
                finalVal = f'{rowValue:.2f}'
            except ValueError:
                pass

        nDict[values[rowCheck]] = finalVal 
    
    numCheck = 0
    for key, value in sorted(nDict.items(), key = lambda x: x[1], reverse=TRUE):
        if numCheck >= n:
            break
        else:
            numCheck += 1
            data = ('# ' + str(numCheck), key, value)
            nTree.insert('', 'end', values=data)
    nTree.insert("", "end")
    nTree.column("Place", minwidth=0, width=50, stretch=NO)


class NormalizationWindow:
    def __init__(self, data):
        self.norm_root = tk.Tk()
        self.norm_root.geometry("1750x750")
        self.norm_root.title("Normalize Data")

        self.top_frame = tk.Frame(self.norm_root, bg='LightBlue', pady="10", padx="10", height='50')
        self.top_frame.pack(side=tk.TOP, fill='x', expand=False)

        self.header_label = tk.Label(self.top_frame, text=" Normalized Values: Select a Method",
                                     bg="white", fg="black", font=('Helvetica', 20))
        self.header_label.pack(fill=tk.X)

        self.top_frame.pack_propagate(0)

        self.middle_frame = tk.Frame(self.norm_root, bg='orange', pady="5", padx="5", height='10')
        self.middle_frame.pack(side=tk.TOP, fill='x', expand=False)

        self.middle_frame2 = tk.Frame(self.middle_frame, bg='orange', height='10')
        self.middle_frame2.pack(side=tk.LEFT, fill='x', expand=False)

        self.pin_check = tk.StringVar(self.norm_root)
        self.pin_box = tk.Checkbutton(self.middle_frame2, text="Pin Outliers", variable=self.pin_check, onvalue='(Pinned)', offvalue="",
                                      command=lambda: self.header_update(""))
        self.pin_box.pack(side=tk.LEFT, padx='10')

        self.method_labels = [" -1, 1 ", " 0, 1 ", " 0, 10 ", " 1, 10 ", " Z-Scores "]
        self.button_dict = {}

        for methods in self.method_labels:
            self.button_dict[methods] = tk.Button(self.middle_frame2, text=methods, padx=10,
                                                command=lambda methods = methods: (self.norm_tree.delete(*self.norm_tree.get_children()), 
                                                NormalizeData(self.pin_check, methods, data, self.norm_tree), 
                                                self.header_update(methods)))
            self.button_dict[methods].pack(side=tk.LEFT, padx=10)
        
        self.space_label = Label(self.middle_frame2, font = ("Helvetica", 24), text="     ", background='orange')
        self.space_label.pack(side=tk.LEFT)

        self.topN_button = tk.Button(self.middle_frame2, text=" Top N ", padx='10', command = self.TopNFrame)
        self.topN_button.pack(side=tk.LEFT, padx=5)

        self.nNum = tk.IntVar(self.norm_root)
        self.nNum.set(int(len(data)/2))

        self.nField = ttk.Entry(self.middle_frame2, textvariable = self.nNum,  width=5, justify=CENTER, font=('Arial', 12))
        self.nField.pack(side=tk.LEFT, padx=1)

        self.nInc = tk.Button(self.middle_frame2, text="▲", font = ("Helvetica", 7, 'bold'), height= 1, padx=0, pady=0, command=lambda: self.nMath(0, 'plus'))
        self.nInc.pack(side=tk.TOP)

        self.nDec = tk.Button(self.middle_frame2, text="▼", font = ("Helvetica", 7, 'bold'),  height= 1, padx=0, pady=0, command=lambda: self.nMath(0, 'minus'))
        self.nDec.pack(side=tk.BOTTOM)

        self.nRadioNum = tk.StringVar(self.norm_root)

        self.nR1 = tk.Radiobutton(self.middle_frame, text='All Numerics ', value = 'All Numerics', variable= self.nRadioNum, font=("Helvetica", 14))
        self.nR1.pack(side=tk.LEFT, padx=3)
        self.nR2 = tk.Radiobutton(self.middle_frame, text='Inputs ', value = 'Inputs', variable= self.nRadioNum,font=("Helvetica", 14))
        self.nR2.pack(side=tk.LEFT, padx=3)
        self.nR3 = tk.Radiobutton(self.middle_frame, text='Outputs ', value = 'Outputs', variable= self.nRadioNum,font=("Helvetica", 14))
        self.nR3.pack(side=tk.LEFT, padx=3)

        self.nRadioNum.set('All Numerics')

        self.reset = tk.Button(self.middle_frame, text=" Reset ", padx=10,
                                                command=lambda: (self.norm_tree.delete(*self.norm_tree.get_children()), 
                                                NormalizeData('', '', data, self.norm_tree), 
                                                self.header_update('R'), self.TopNClose()))
        self.reset.pack(side=tk.RIGHT, padx=5)


        self.nFrame = tk.Frame(self.norm_root, bg='sea green', padx=0, pady=10)

        self.nClose = tk.Button(self.nFrame, text="X", font = ('Helvetica', 10, 'bold'), command= lambda: self.TopNClose())
        self.nClose.pack(side=tk.RIGHT, anchor=tk.NE, padx=0)

        self.bottom_frame = ttk.Frame(self.norm_root)
        self.bottom_frame.pack(side = tk.RIGHT, expand=tk.TRUE, fill=tk.BOTH)

        self.nHead = tk.Label(self.nFrame, text= " Top " + str(self.nNum.get()) + " for " + str(self.nRadioNum.get()),
                                            bg="white", fg="black", font=('Helvetica', 18), pady=5, justify=tk.CENTER)
        self.nHead.pack(side=tk.TOP, pady=5, padx=5)

        self.nTreeFrame = tk.Frame(self.nFrame, padx=10, pady=10)
        self.nTreeFrame.pack(side = tk.TOP, expand=tk.TRUE, fill=tk.BOTH, padx=5)

        self.nTree = ttk.Treeview(self.nTreeFrame, columns=('Place', colnames[0], 'Score'), show='headings')
        


        self.nTree.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
        
        self.nScroll = ttk.Scrollbar(self.nTree, orient="vertical", command=self.nTree.yview)
        self.nScroll2 = ttk.Scrollbar(self.nTree, orient="horizontal", command=self.nTree.xview)
        self.nTree.configure(yscrollcommand=self.nScroll.set)
        self.nTree.configure(xscrollcommand=self.nScroll2.set)

        self.nScroll.pack(side=RIGHT, fill="y")
        self.nScroll2.pack(side=BOTTOM, fill="x")

        self.norm_tree = ttk.Treeview(self.bottom_frame, columns=colnames, show='headings')

        self.scrollbar = ttk.Scrollbar(self.norm_tree, orient="vertical", command=self.norm_tree.yview)
        self.scrollbar2 = ttk.Scrollbar(self.norm_tree, orient="horizontal", command=self.norm_tree.xview)
        self.norm_tree.configure(yscrollcommand=self.scrollbar.set)
        self.norm_tree.configure(xscrollcommand=self.scrollbar2.set)

        self.norm_tree.pack(side="bottom", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar2.pack(side="bottom", fill="x")

        self.norm_tree.bind("<Double-1>", self.OnDoubleClick)

        for colindex, col in enumerate(colnames):
            self.norm_tree.heading("#" + str(colindex + 1), text=col)
        for row in data:
            if row == colnames:
                pass
            else:
                self.norm_tree.insert("", "end", values=row)
        
        self.norm_root.mainloop()

    def TopNFrame(self): 

        if self.nMath(1, ''):
            TopNCal(self.nTree, self.norm_tree, self.nNum.get(), "")
            
            
            self.nHead.config(text= " Top " + str(self.nNum.get()) + " for " + str(self.nRadioNum.get()),
                                bg="white", fg="black", font=('Helvetica', 18), pady=5, justify=tk.CENTER, width=25)
            self.nFrame.pack(side = tk.LEFT, expand=tk.FALSE, fill=tk.Y)

    def TopNClose(self):
        self.nFrame.forget()

    def OnDoubleClick(self, event):
        item = self.norm_tree.selection()
        if item:
            values = self.norm_tree.item(item[0], "values")

            print(values)


    def header_update(self, norm_type):
        if norm_type == '':
            return
        elif norm_type == 'R':
            self.header_label.config(text=" Normalized Values: Select a Method")
        else:
            self.header_label.config(text=" Normalized Values: " + norm_type + " " + str(self.pin_check.get()))

    def nMath(self, x, math):
        try:
            self.nNum.get()
        except TclError:
            messagebox.showerror(" Invaild Entry ", " The value of N must be a number ", parent = self.norm_root)
            return 0

        if self.nNum.get() > len(data) - 1 or self.nNum.get() < 1:
            messagebox.showerror(" Value out of Range ", " The value of N must be between 1 and " + str(len(data) - 1) + " ", parent = self.norm_root)

            return 0
        else:
            if x == 0 and math == 'plus':
                self.nNum.set(self.nNum.get() + 1)
            elif x == 0 and math == 'minus':
                self.nNum.set(self.nNum.get() - 1)
            else:
                return 1


        
if __name__ == "__main__":
    root=tk.Tk()
    root.geometry("1500x500")
    root.pack_propagate(0)
    CSVReader(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
