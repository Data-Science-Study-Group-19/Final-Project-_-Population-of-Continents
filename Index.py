import pandas as pd

# Class to represent a Table also place to create the functions for 3.1
class Table:
    def __init__(self, data, name):
        self.data = data
        self.name = name
        self.data["Table_Name"] = name  # Add table name as a column

    def save_to_csv(self, filename):
        self.data.to_csv(filename, index=False)
        print(f"{self.name} saved to {filename}")

    def display_info(self):
        print(f"Table Name: {self.name}")
        print(self.data.head())

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_continents_and_continental_subregions_by_population"

# Read all tables from the page
tables = pd.read_html(url, header=0)

# Display the number of tables found
print(f"Number of tables found: {len(tables)}")

# Select a range of tables
selected_tables = tables[3:28]

# List to store table objects
table_objects = []

# Create an object for each table and add it to the list
for i, table in enumerate(selected_tables, start=0):
    table_name = f"Table {i}"
    table_obj = Table(data=table, name=table_name)
    table_objects.append(table_obj)

# Combine DataFrames from all table objects
combined_df = pd.concat([table_obj.data for table_obj in table_objects], ignore_index=True)

# Removing unwanted chars
combined_df = combined_df.replace('%', '', regex=True)
combined_df = combined_df.replace('—', '0', regex=True)

# Save the combined DataFrame to a single CSV file
combined_df.to_csv("TestSubregions.csv", index=True)

# How to display a table
table_10 = table_objects[10]  # Accessing the 10th table
table_10.display_info()
