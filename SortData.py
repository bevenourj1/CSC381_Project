def sort_data(data, sort_columns, ascending_flags):
    if len(sort_columns) != len(ascending_flags):
        raise ValueError(
            "The number of sort columns and ascending flags must match.")

    sorted_data = data[:]
    for column_index, ascending in zip(sort_columns, ascending_flags):
        sorted_data = sorted(
            sorted_data, key=lambda x: x[column_index], reverse=not ascending)
    return sorted_data


if __name__ == "__main__":
    # Assign your data to csv_data, columns to column_number, and sorting order to ascending_flags
    csv_data = [
        ["Arizona Cardinals", 5499, 4.8, 5.1, 4.3, 65.2, 37,
            5931, 5.5, -5, 6.2, 4.5, 69.8, 36, 52, 0.235, -6.4],
        ["Atlanta Falcons", 5417, 5.4, 6, 4.9, 61.9, 38, 6156,
            5.7, -4, 6.8, 4.4, 66.3, 21, 41, 0.412, -1.2],
        ["Baltimore Ravens", 5760, 5.5, 5.8, 5.2, 61.5, 34,
            5513, 5.3, 4, 6.2, 3.9, 66.4, 48, 32, 0.588, 2.1]
    ]

    column_number = [0, 1]  # Sort by the second and third columns
    ascending_flags = [True, False]  # Ascending for the first column, descending for the second column

    # Sort the data based on user specifications
    sorted_data = sort_data(csv_data, column_number, ascending_flags)
