# DevGrp One
# CSC 381

import os 
import csv
import copy

os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Open CSV
with open("NFLTeams2022.csv") as csv_file:
    data = list(csv.reader(csv_file, delimiter=','))

# Create copies of the CSV file
# Had to import copy, python does pass-by-reference so a deepcopy is done for a real copy
data_Normalize_ZeroOne = copy.deepcopy(data)
data_Normalize_NegOneOne = copy.deepcopy(data)
data_Normalize_ZeroTen = copy.deepcopy(data)
data_Normalize_OneTen = copy.deepcopy(data)

# Loop through CSV file
for x in range(len(data[1])):

    # Used to track the current row
    row_count = 1

    # This is used to check if the item in the column is numeric
    # It looks at the sting value stored there at checks the last character in the string
    # Example: 1.234 | Checks '4' and then assumes the column is numeric
    # Example: Arizona Cardinals | Checks 's' and then assumes the column is non-numeric
    size = len(data[1][x])
    if data[1][x][size - 1].isdigit():

        # List is created that holds all the data in the column
        # Removes the first index since that is the headers
        # Converts list into integers before sorting 
        temp_col = [sub[x] for sub in data]
        temp_col.pop(0)
        temp_col = [eval(i) for i in temp_col]
        temp_col.sort()
            
        # Loops while there is still a row in data and fills it in with Normalized Data
        # Breaks when it is at the final row of the CSV file
        while True:
            data_Normalize_ZeroOne[row_count][x] = f'{(float(data[row_count][x]) - float(min(temp_col))) / (float(max(temp_col)) - float(min(temp_col))):.4f}'
            data_Normalize_OneTen[row_count][x] = f'{1 + (float(data[row_count][x]) - float(min(temp_col))) / (float(max(temp_col)) - float(min(temp_col))) * 9:.4f}'
            data_Normalize_ZeroTen[row_count][x] = f'{(float(data[row_count][x]) - float(min(temp_col))) / (float(max(temp_col)) - float(min(temp_col))) * 10:.4f}'
            data_Normalize_NegOneOne[row_count][x] = f'{(float(data[row_count][x]) - float(min(temp_col))) / (float(max(temp_col)) - float(min(temp_col))) * 2 - 1:.4f}'

            row_count += 1
            if row_count == len(data):
                break
            

# Display the first row of all the normalized data and original data
print(data_Normalize_ZeroOne[1])
print(data_Normalize_OneTen[1])
print(data_Normalize_ZeroTen[1])
print(data_Normalize_NegOneOne[1])
print(data[1])