import pandas as pd

# Class to represent a Table also place to create the functions for 3.1
class Table:
    def __init__(self, data, name, **attributes):
        self.data = data
        self.name = name
        for key, value in attributes.items():
            setattr(self, key, value)
        self.extract_attributes()  # Automatically extract and set attributes

    def extract_attributes(self):
        if 'Year' in self.data.columns:
            self.year = self.data['Year'].tolist()
        if 'Pop.' in self.data.columns:
            self.population = self.data['Pop.'].tolist()
        if '±% p.a.' in self.data.columns:
            self.growth_rate = self.data['±% p.a.'].tolist()

    def save_to_csv(self, filename):
        self.data.to_csv(filename, index=False)
        print(f"{self.name} saved to {filename}")

    def display_info(self):
        print(f"Table Name: {self.name}")
        for key, value in vars(self).items():
            if key not in ['data', 'name']:
                print(f"{key}: {value}")
        print(self.data.head())
    
    def display_subset(self, row_start, row_end, col_start, col_end):
        subset = self.data.iloc[row_start:row_end, col_start:col_end]
        print(f"Subset of {self.name}:")
        print(subset)

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
    additional_attributes = {"source_url": url, "index": i}
    table_obj = Table(data=table, name=table_name, **additional_attributes)
    table_objects.append(table_obj)

# Combine DataFrames from all table objects
combined_df = pd.concat([table_obj.data for table_obj in table_objects], ignore_index=True)

# Removing unwanted chars
combined_df = combined_df.replace('%', '', regex=True)
combined_df = combined_df.replace('—', '0', regex=True)

# Save the combined DataFrame to a single CSV file
combined_df.to_csv("TestSubregions.csv", index=True)

# Example: Display user-defined subset of the 10th table
table_10 = table_objects[10]  # Accessing the 10th table
row_start, row_end = 0, 2  # User input for rows
col_start, col_end = 0, 2  # User input for columns
table_10.display_subset(row_start, row_end, col_start, col_end)
