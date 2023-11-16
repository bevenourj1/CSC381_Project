# Python program to create a table

from tkinter import *
import csv
import os
global data

os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open('real college data for 381.csv') as csv_file:
    data = list(csv.reader(csv_file, delimiter=','))

import tkinter as tk

class ColorWindow:
    def __init__(self, root):

        self.canvas = tk.Canvas(root, bg='white')
        self.canvas.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        self.scrollbar_y = tk.Scrollbar(self.canvas, command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar_y.set)
        self.scrollbar_x = tk.Scrollbar(self.canvas, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.config(xscrollcommand=self.scrollbar_x.set)


        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        for col, header in enumerate(data[0]):
            x1 = col * 300
            y1 = 0
            x2 = (col + 1) * 300
            y2 = 30
            x3 = round((x1 + x2) / 2)
            y3 = round((y1 + y2) / 2)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='lightgray')
            self.canvas.create_text(x3, y3, text=header, font=('bold'))

        for row, row_data in enumerate(data[1:], start=1):
            for col, value in enumerate(row_data):
                column_values = [row[col] for row in data]
                column_values.pop(0)
                x1 = col * 300
                y1 = row * 30
                x2 = (col + 1) * 300
                y2 = (row + 1) * 30
                x3 = round((x1 + x2) / 2)
                y3 = round((y1 + y2) / 2)
                try:
                    column_values = [float(x) for x in column_values]
                    column_values.sort()

                    cutNum = round(len(data) * 0.1)

                    maxVal = max(column_values)
                    minVal = min(column_values)
                    


                    # if float(value) >= column_values[(len(data) - 1) - cutNum]:
                    #     self.canvas.create_rectangle(x1, y1, x2, y2, fill='light green')
                    #     self.canvas.create_text(x3, y3, text=value)
                    #     continue
                    # if float(value) <= column_values[cutNum]:
                    #     self.canvas.create_rectangle(x1, y1, x2, y2, fill='IndianRed2')
                    #     self.canvas.create_text(x3, y3, text=value)
                    #     continue

                    if float(value) == maxVal:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill='light green')
                        self.canvas.create_text(x3, y3, text=value)
                        continue
                    if float(value) == minVal:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill='IndianRed2')
                        self.canvas.create_text(x3, y3, text=value)
                        continue
                    
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')
                    self.canvas.create_text(x3, y3, text=value)
                except ValueError:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')
                    self.canvas.create_text(x3, y3, text=value)

        self.canvas.config(scrollregion=(0, 0, len(data[0]) * 300 + 10, len(data) * 30 + 10))

root = tk.Tk()
root.title("Colored Data")
root.geometry('2000x1000')

color_root = ColorWindow(root)

root.mainloop()

















