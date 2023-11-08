import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import csv
import copy
import statistics

os.chdir(os.path.dirname(os.path.realpath(__file__)))

colnames = []
select_nor = ["0,1", "1,10", "0,10", "-1,1", "Z-Scores"]

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

            delete_command()
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

        def UploadAction(event=None):
                delete_command()
                global colnames
                global data
                data = []
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

                    for colindex, col in enumerate(colnames):
                        self.tree.heading("#" + str(colindex + 1), text=col)   

                    for row in csv_reader:
                        self.tree.insert("", "end", values=row)
                with open(filename) as csv_file:
                    data = list(csv.reader(csv_file, delimiter=','))

        def delete_command():
            for col in self.tree['columns']:
                self.tree.heading(col, text='')
            self.tree.delete(*self.tree.get_children())

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



        self.bottomFrame = ttk.Frame(self)
        self.bottomFrame.pack(expand=tk.YES, fill=tk.BOTH)

    
        self.tree = ttk.Treeview(self.bottomFrame,columns=colnames, show='headings')

        self.scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.scrollbar2 = ttk.Scrollbar(self.tree, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand= self.scrollbar.set)
        self.tree.configure(xscrollcommand= self.scrollbar2.set)

                # Pack the Treeview and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar2.pack(side="bottom", fill="x")

if __name__ == "__main__":
    root=tk.Tk()
    root.geometry("1500x500")
    root.pack_propagate(0)
    CSVReader(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
    
