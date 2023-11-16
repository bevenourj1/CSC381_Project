import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import os
import csv
import copy
import statistics
import types
import re
from itertools import chain
os.chdir(os.path.dirname(os.path.realpath(__file__)))

colnames = []
select_nor = ["0,1", "1,10", "0,10", "-1,1", "Z-Scores"]
props = ["high good", "low good", "descriptive"]
#io = ["input", "output"]
standard_updated_index = 0
standard_data = []
colinput_unique = []
coloutput_unique = []
colchoices = []
col_io_choices = []
col_input_choices = []
col_output_choices = []
desc_rows = []
similarity_data = []
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
        
        curr_compare_row = tk.StringVar(self) 
        similar_choice = tk.StringVar(self)
        similarspecify_choice = tk.StringVar(self)

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
                global desc_rows
                global standard_data
                global standard_updated_index

                filename = filedialog.askopenfilename()
                # Open and read the CSV file
                with open(filename, "r") as csv_file:
                    csv_reader = csv.reader(csv_file)


                    colnames = next(csv_reader)
                    self.tree.configure(columns=colnames)    
                        

                    if len(colprops) == 0:
                        colprops = {colname: None for colname in colnames}
                    
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
                    
                    for i, row in enumerate(data):
                        if i > 0:
                            desc_rows.append(row[0])
                    regexp = re.compile('[a-z|A-Z]')

                    
                    
                    for row in data:
                        temp_row = []
                        for element in row:      
                            if regexp.search(element) == None:
                                temp_row.append(element)
                            else:
                                standard_updated_index += 1
                        if len(temp_row) != 0:
                            similarity_data.append(temp_row)
                    #print(similarity_data)
                    standard_updated_index = (len(data[0]) - 1) - (len(similarity_data[0]) - 1)
                    print (standard_updated_index)
                    standard_data = copy.deepcopy(similarity_data)

                    for x in range(len(standard_data[1])):

                        row_count = 0
                        temp_col = [sub[x] for sub in standard_data]
                        temp_col.pop(0)
                        temp_col = list(map(float, temp_col))
                        temp_col.sort()
                        while row_count != len(standard_data):
                            standard_data[row_count][x] = f'{1 + (float(standard_data[row_count][x]) - min(temp_col)) / (max(temp_col) - min(temp_col)) * 9:.4f}'
                            row_count += 1

                #print(standard_data)
                set_desc_compare()

        def norm_delete_command():
            for col in self.tree['columns']:
                self.tree.heading(col, text='')
            self.tree.delete(*self.tree.get_children())

        def delete_command():
            global colprops
            global oldList
            global col_io
            global col_inputs
            global standard_data
            global similarity_data
            global col_outputs
            global colnames
            colnames = []
            for col in self.tree['columns']:
                self.tree.heading(col, text='')
            self.tree.delete(*self.tree.get_children())
            oldList = False
            colprops = {}
            similarity_data = []
            standard_data = []
            col_io = {}
            col_inputs = {}
            col_outputs = {}

        def set_desc_compare():
            global desc_rows
            curr_compare_row.set("Select Comparison Row")
            similar_choice.set("Select Similarity Method")
            similarspecify_choice.set("Select Similarity Comparison Columns")
            desc_drop = tk.OptionMenu(self.rowFrame, 
                                      curr_compare_row, 
                                      *desc_rows) 
            
            similar_method = ["Crow Flies (Difference Squared)", "City Blocks (Absolute Value)"]
            
            
            method_drop = tk.OptionMenu(self.rowFrame, 
                                      similar_choice, 
                                      *similar_method)

            similar_specify = ["All Columns", "Input Columns", "Output Columns"]
            specify_drop = tk.OptionMenu(self.rowFrame, 
                                      similarspecify_choice, 
                                      *similar_specify)  
    
            getSim = tk.Button(self.rowFrame, text='Get Most Similar Row', command=get_most_similar)

            
            desc_drop.pack(side=tk.TOP)
            method_drop.pack(side=tk.TOP)
            specify_drop.pack(side=tk.TOP)
            getSim.pack(side=tk.TOP)

        def get_most_similar():

            global desc_rows
            global standard_data
            global standard_updated_index
            global colnames
            global col_inputs
            global col_outputs
            global colinput_unique
            global coloutput_unique
            temp = 0
            colinput_indices = []
            coloutput_indices = []
            similarity_scores = {row: 0 for row in desc_rows}
            selected_index = desc_rows.index(curr_compare_row.get())
            compare_row = standard_data[selected_index]

            colinput_unique = list(sorted(set(chain(*col_inputs.values()))))
            coloutput_unique = list(sorted(set(chain(*col_outputs.values()))))
            print(colinput_unique)
            if similarspecify_choice.get() == "All Columns":
                for i, row in enumerate(standard_data):
                    temp = 0
                    if i == selected_index:
                        pass
                    else:
                        for x, element in enumerate(row):
                            if(similar_choice.get() == "City Blocks (Absolute Value)" or similar_choice.get() == "Select Similarity Method"):
                                temp += abs(float(compare_row[x]) - float(element))
                                similarity_scores[desc_rows[i]] = temp
                            elif(similar_choice.get() == "Crow Flies (Difference Squared)"):
                                temp += pow((float(compare_row[x]) - float(element)), 2)
                                similarity_scores[desc_rows[i]] = temp
            
            if similarspecify_choice.get() == "Input Columns":
                for index, cols in enumerate(colnames):
                    for inputcols in colinput_unique:
                        if inputcols == cols:
                            colinput_indices.append(index)
                for i, row in enumerate(standard_data):
                    temp = 0
                    if i == selected_index:
                        pass
                    else:
                        for x, element in enumerate(row):
                                for index in colinput_indices:

                                    if(index == x + standard_updated_index):
                                        if(similar_choice.get() == "City Blocks (Absolute Value)" or similar_choice.get() == "Select Similarity Method"):
                                            temp += abs(float(compare_row[x]) - float(element))
                                            similarity_scores[desc_rows[i]] = temp
                                        elif(similar_choice.get() == "Crow Flies (Difference Squared)"):
                                            temp += pow((float(compare_row[x]) - float(element)), 2)
                                            similarity_scores[desc_rows[i]] = temp

            if similarspecify_choice.get() == "Output Columns":
                for index, col in enumerate(colnames):
                    for outputcol in coloutput_unique:
                        if outputcol == col:
                            coloutput_indices.append(index)
                for i, row in enumerate(standard_data):
                    temp = 0
                    if i == selected_index:
                        pass
                    else:
                        for x, element in enumerate(row):
                                for index in coloutput_indices:
                                    if(index == x + standard_updated_index):
                                        if(similar_choice.get() == "City Blocks (Absolute Value)" or similar_choice.get() == "Select Similarity Method"):
                                            temp += abs(float(compare_row[x]) - float(element))
                                            similarity_scores[desc_rows[i]] = temp
                                        elif(similar_choice.get() == "Crow Flies (Difference Squared)"):
                                            temp += pow((float(compare_row[x]) - float(element)), 2)
                                            similarity_scores[desc_rows[i]] = temp

            
            similarity_scores = {k: v for k, v in sorted(similarity_scores.items(), key=lambda item: item[1])}       
             
            Current = Toplevel(self)
            Current.title((desc_rows[selected_index]) + "'s Most Similar to Least Similar rows from " + similarspecify_choice.get() + " using " + similar_choice.get())
            Current.geometry('1024x768')
            
            similar_frame = tk.Frame(Current, bg="white", pady="10", padx="10", 
                            width="200", height="150")
            similar_frame = ttk.Frame(Current)
            similar_frame.pack(expand=tk.YES, fill=tk.BOTH)
            #if(similarspecify_choice.get() == "Input Columns"):
             #   similar_tree = ttk.Treeview(similar_frame,columns=colinput_unique, show='headings')

            similar_tree = ttk.Treeview(similar_frame,columns=colnames, show='headings')

            similar_tree.configure(columns=colnames)
            for i, col in enumerate( similar_tree['columns']):
                for index in colinput_indices:
                    if(i == index):
                        similar_tree.heading(col, text=colnames[i])
   
            scrollbar = ttk.Scrollbar(similar_tree, orient="vertical", command=similar_tree.yview)
            scrollbar2 = ttk.Scrollbar(similar_tree, orient="horizontal", command=similar_tree.xview)
            similar_tree.configure(yscrollcommand= scrollbar.set)
            similar_tree.configure(xscrollcommand= scrollbar2.set)

            similar_tree.pack(side="left", fill="both", expand=True)
            similar_tree.pack(side="bottom", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            scrollbar2.pack(side="bottom", fill="x")


            for desc_row in similarity_scores:
                for row in data:
                    if row[0] == desc_row:
                       similar_tree.insert("", "end", values=row)
            
                      

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
        self.drop.pack(side=tk.TOP)

        self.dropFrame.pack()
        self.dropFrame.pack_propagate(0)

        self.rowFrame = tk.Frame(self,bg="white", pady="10", padx="10", 
                             width = "200", height="70")

        self.rowFrame.pack(side=tk.TOP)   
        self.rowFrame.pack()

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
