from tabulate import tabulate
import pandas as pd

# Extracting the data from Wikipedia by using the pandas library
url = "https://en.wikipedia.org/wiki/List_of_continents_and_continental_subregions_by_population"
tables = pd.read_html(url)

# When extracting data from the Wikipedia page, the data is unstructured and needs to be cleaned
# Table for all regions
region_tables = tables[3:]  
region = pd.concat(region_tables, ignore_index=True)
region.to_csv("region.csv", index=False)


# Renaming the columns to make them identical
region = region.rename(columns={'Pop.': 'Population'})


# The table for regions dont have the same structure as the other tables. 
# The table for regions needs to be cleaned and structured
# The table do not have region name but just Year and Population. 
# First step is therefore to create a new column with the Region_nr where each unique region is assigned a number based on repeated data from 1950 to 2021
region['Region_nr'] = (region['Year'] == 1950).cumsum()

# Define mapping between region number and region name 
region_mapping = {
    1: "Eastern Africa",
    2: "Middle Africa",
    3: "Northern Africa",
    4: "Southern Africa",
    5: "Western Africa",
    6: "Total Africa",
    7: "Total Americas",
    8: "Caribbean",
    9: "Central America",
    10: "North America",
    11: "Total North America",
    12: "Total South America",
    13: "Central Asia",
    14: "Eastern Asia",
    15: "South-Eastern Asia",
    16: "Southern Asia",
    17: "Western Asia",
    18: "Total Asia",
    19: "Eastern Europe",
    20: "North Europe",
    21: "Southern Europe",
    22: "Western Europe",
    23: "Total Europe",
    24: "Total Oceania",
    25: "Total World",
}

# Adding a new column 'Region' by mappiung region number with the name 
region['Region'] = region['Region_nr'].map(region_mapping)

# Defining the continent identifiers from the list
continent_identifiers = {6, 11, 12, 18, 23, 24, 25}

# Extracting the continent data with the identified continent identifiers
continent = region[region['Region_nr'].isin(continent_identifiers)].copy()

continent = continent.rename(columns={'Region': 'Continent'})

# Dropping the continent rows from the original DataFrame 
region = region[~region['Region_nr'].isin(continent_identifiers)].copy()

# Saving the continent DataFrame
continent.to_csv("continent.csv", index=False)

class Region:
    def __init__(self, data):
        
        # Initialize the Region class with a DataFrame containing Year, Population, and Region.
        self.data = data
    
    """
    This function was working too, but it once again made the class/subclass structure unnecessary
    One could simply use continent dataframe with the Region class and get the same result
    def area_type(self):
        
        if 'Region' in self.data.columns:
            area_type = "region"
            return area_type
        elif 'Continent' in self.data.columns:
            area_type = "continent"
            return area_type
    """
    def area_type(self):
        
        # Assigns a variable with 'region' to help make methods dynamic
        area_type = 'region'
        return area_type

    def display_population(self, area_name, year):
        
        area_type = self.area_type()
        
        # Display the population of a specific region in a specific year.
        area_data = self.data[(self.data[area_type.capitalize()] == area_name) & (self.data['Year'] == year)]
        if not area_data.empty:
            population = area_data['Population'].iloc[0]
            print(f"Population of {area_name} in {year}: {population:,}")
        else:
            print(f"No data available for {area_name} in {year}.")

    def population_comparison(self, area_name1, area_name2, year):
        
        area_type = self.area_type()
        
        # Compares the population between two regions in a specific year.
        area_data1 = self.data[(self.data[area_type.capitalize()] == area_name1) & (self.data['Year'] == year)]
        area_data2 = self.data[(self.data[area_type.capitalize()] == area_name2) & (self.data['Year'] == year)]
        if not area_data1.empty and not area_data2.empty:
            population1 = area_data1['Population'].iloc[0]
            population2 = area_data2['Population'].iloc[0]
            print(f"Population in {area_name1} in {year}: {population1:,}") 
            print(f"Population in {area_name2} in {year}: {population2:,}")
        else: 
            print(f"Data for one or both {area_type}s for the specified year is not available.")
        if population1 > population2:
            print(f"{area_name1}s population was greater than {area_name2}s population.")
        elif population2 > population1:
            print(f"{area_name2}s population was greater than {area_name1}s population.")
        elif population1 == population2:
            print(f"You cannot compare the same {area_type}")
        

    def population_sort(self, year):
        
        area_type = self.area_type()
        
        # Sort regions by population size in a specific year
        unsorted_data = self.data[(self.data['Year'] == year)]
        if not unsorted_data.empty:
            sorted_data = unsorted_data.sort_values(by=['Population'], ascending=False)
            print(f"Here are {area_type}s sorted population in the year {year}:\n{sorted_data}")
        else:
            print(f"No data available for {area_type}s in {year}.")
        

    def growth_calculator(self, area_name, year):
        
        area_type = self.area_type()
        
        # Calculates the annual growth rate of a region for a given year,
        # accounting for datasets where population is recorded every 10 years.
        
        # Filter data for the specified region
        area_data = self.data[self.data[area_type.capitalize()] == area_name]

        # Ensure the requested year exists in the data
        if year not in area_data['Year'].values:
            print(f"No data available for {area_name} in {year}.")
            return None

        # Find the closest previous year with data
        previous_year_data = area_data[area_data['Year'] < year].sort_values(by='Year', ascending=False)

        if previous_year_data.empty:
            print(f"No previous data available for {area_name} before {year}.")
            return None

        # Get the populations for the current and previous years
        current_population = area_data[area_data['Year'] == year]['Population'].iloc[0]
        previous_population = previous_year_data['Population'].iloc[0]
        previous_year = previous_year_data['Year'].iloc[0]

        # Calculate growth rate
        growth_rate = ((current_population - previous_population) / previous_population) * 100

        self.data.loc[(self.data[area_type.capitalize()] == area_name) & (self.data['Year'] == year), 'Growth Rate'] = growth_rate

        # Display or return growth rate
        print(f"Growth rate for {area_name} in {year}: {growth_rate:.2f}%")
        return growth_rate
    
    
    def growth_comparison(self, area1, area2, year):
        
        # Compares the growth rate between two areas in a specific year.
        growth1 = self.growth_calculator(area1, year)
        growth2 = self.growth_calculator(area2, year)

        if growth1 is not None and growth2 is not None:
            if growth1 > growth2:
                print(f"{area1} had a higher growth rate ({growth1:.2f}%) than {area2} ({growth2:.2f}%) in {year}.")
            elif growth2 > growth1:
                print(f"{area2} had a higher growth rate ({growth2:.2f}%) than {area1} ({growth1:.2f}%) in {year}.")
            else:
                print(f"{area1} and {area2} had the same growth rate ({growth1:.2f}%) in {year}.")
        else:
            print("Comparison could not be made due to insufficient data.")

    
    def growth_sort(self, year):
        
        area_type = self.area_type()
        
        # Sorts the DataFrame by growth rate for a specific year and returns the sorted DataFrame.
        
        # Ensure the 'Growth Rate' column exists
        if 'Growth Rate' not in self.data.columns:
            self.data['Growth Rate'] = None

        # Calculate growth rate for all areas for the specified year
        areas = self.data[area_type.capitalize()].unique()
        for area in areas:
            self.growth_calculator(area, year)  # Updates the 'Growth Rate' column dynamically

        # Filter rows for the specified year and sort by 'Growth Rate'
        year_data = self.data[self.data['Year'] == year]
        sorted_data = year_data.sort_values(by='Growth Rate', ascending=False)

        print(f"{area_type.capitalize()}s sorted by growth rate in {year}:")
        print(tabulate(sorted_data))

        return sorted_data

# subclass Continent inherits from Region
class Continent(Region):
    
    # Initialize subclass Continent with all methods from Region
    def __init__(self, data):
        self.data = data
        Region.__init__(self, data)
    
    def area_type(self):
        
        # This method overwrites the one in Region to allow the other methods
        # to work dynamically with regions and continents
        
        # Assigns a variable with continent for use in dynamic methods
        area_type = 'continent'
        return area_type
    
def menu(region, continent):
    # Initialize classes with provided dataframes
    region_instance = Region(region)
    continent_instance = Continent(continent)

    while True:
        print("\nWelcome to the Population Analyzer by Engin, Michael, Søren & Jeppe")
        print("Menu:")
        print("1. Display the population of a region or continent.")
        print("2. Compare the population between two regions or continents.")
        print("3. Sort regions or continents by population size.")
        print("4. Calculate the annual growth rate of regions or continents.")
        print("5. Compare the growth rate between two regions or continents.")
        print("6. Sort regions or continents by growth rate.")
        print("7. Exit")
        
        try:
            choice = int(input("Choose an option: "))
            if choice == 7:
                print("Exiting program.")
                break

            def analyze_more():
                while True:
                    more_analysis = input("\nDo you want to analyze more data in this context? (yes/no): ").strip().lower()
                    if more_analysis == "yes":
                        return True
                    elif more_analysis == "no":
                        return False
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")

            if choice == 1:  # Display population
                while True:
                    print("\nDo you want to display population for:")
                    print("1. Region")
                    print("2. Continent")
                    sub_choice = int(input("Choose 1 for Region or 2 for Continent: "))

                    if sub_choice == 1:  # Regions
                        while True:
                            print("\nAvailable Regions:")
                            for i, reg in enumerate(region['Region'].unique(), 1):
                                print(f"{i}. {reg}")
                            region_choice = int(input("Select a region by number: "))
                            area_name = region['Region'].unique()[region_choice - 1]

                            print("\nAvailable Years:")
                            for i, yr in enumerate(region['Year'].unique(), 1):
                                print(f"{i}. {yr}")
                            year_choice = int(input("Select a year by number: "))
                            year = region['Year'].unique()[year_choice - 1]

                            region_instance.display_population(area_name, year)
                            if not analyze_more():
                                break

                    elif sub_choice == 2:  # Continents
                        while True:
                            print("\nAvailable Continents:")
                            for i, cont in enumerate(continent['Continent'].unique(), 1):
                                print(f"{i}. {cont}")
                            continent_choice = int(input("Select a continent by number: "))
                            area_name = continent['Continent'].unique()[continent_choice - 1]

                            print("\nAvailable Years:")
                            for i, yr in enumerate(continent['Year'].unique(), 1):
                                print(f"{i}. {yr}")
                            year_choice = int(input("Select a year by number: "))
                            year = continent['Year'].unique()[year_choice - 1]

                            continent_instance.display_population(area_name, year)
                            if not analyze_more():
                                break

                    else:
                        print("Invalid choice. Please choose 1 for Region or 2 for Continent.")
                        continue
                    break

            elif choice == 2:  # Compare population
                while True:
                    print("\nDo you want to compare populations for:")
                    print("1. Region")
                    print("2. Continent")
                    sub_choice = int(input("Choose 1 for Region or 2 for Continent: "))

                    if sub_choice == 1:
                        while True:
                            print("\nAvailable Regions:")
                            for i, reg in enumerate(region['Region'].unique(), 1):
                                print(f"{i}. {reg}")
                            region_choice1 = int(input("Select the first region by number: "))
                            region_choice2 = int(input("Select the second region by number: "))
                            area_name1 = region['Region'].unique()[region_choice1 - 1]
                            area_name2 = region['Region'].unique()[region_choice2 - 1]

                            print("\nAvailable Years:")
                            for i, yr in enumerate(region['Year'].unique(), 1):
                                print(f"{i}. {yr}")
                            year_choice = int(input("Select a year by number: "))
                            year = region['Year'].unique()[year_choice - 1]

                            region_instance.population_comparison(area_name1, area_name2, year)
                            if not analyze_more():
                                break

                    elif sub_choice == 2:
                        while True:
                            print("\nAvailable Continents:")
                            for i, cont in enumerate(continent['Continent'].unique(), 1):
                                print(f"{i}. {cont}")
                            continent_choice1 = int(input("Select the first continent by number: "))
                            continent_choice2 = int(input("Select the second continent by number: "))
                            area_name1 = continent['Continent'].unique()[continent_choice1 - 1]
                            area_name2 = continent['Continent'].unique()[continent_choice2 - 1]

                            print("\nAvailable Years:")
                            for i, yr in enumerate(continent['Year'].unique(), 1):
                                print(f"{i}. {yr}")
                            year_choice = int(input("Select a year by number: "))
                            year = continent['Year'].unique()[year_choice - 1]

                            continent_instance.population_comparison(area_name1, area_name2, year)
                            if not analyze_more():
                                break

                    else:
                        print("Invalid choice. Please choose 1 for Region or 2 for Continent.")
                        continue
                    break

            elif choice == 3:  # Sort regions or continents by population size
                while True:
                    print("\nDo you want to sort by population size for:")
                    print("1. Region")
                    print("2. Continent")
                    sub_choice = int(input("Choose 1 for Region or 2 for Continent: "))

                    if sub_choice == 1:
                        print("\nAvailable Years:")
                        for i, yr in enumerate(region['Year'].unique(), 1):
                            print(f"{i}. {yr}")
                        year_choice = int(input("Select a year by number: "))
                        year = region['Year'].unique()[year_choice - 1]

                        region_instance.population_sort(year)
                    elif sub_choice == 2:
                        print("\nAvailable Years:")
                        for i, yr in enumerate(continent['Year'].unique(), 1):
                            print(f"{i}. {yr}")
                        year_choice = int(input("Select a year by number: "))
                        year = continent['Year'].unique()[year_choice - 1]

                        continent_instance.population_sort(year)
                    else:
                        print("Invalid choice. Please choose 1 for Region or 2 for Continent.")
                        continue

                    if not analyze_more():
                        break

            elif choice == 4:  # Calculate growth rate
                while True:
                    print("\nDo you want to calculate growth rate for:")
                    print("1. Region")
                    print("2. Continent")
                    sub_choice = int(input("Choose 1 for Region or 2 for Continent: "))

                    if sub_choice == 1:
                        print("\nAvailable Regions:")
                        for i, reg in enumerate(region['Region'].unique(), 1):
                            print(f"{i}. {reg}")
                        region_choice = int(input("Select a region by number: "))
                        area_name = region['Region'].unique()[region_choice - 1]

                        print("\nAvailable Years:")
                        for i, yr in enumerate(region['Year'].unique(), 1):
                            print(f"{i}. {yr}")
                        year_choice = int(input("Select a year by number: "))
                        year = region['Year'].unique()[year_choice - 1]

                        region_instance.growth_calculator(area_name, year)
                    elif sub_choice == 2:
                        print("\nAvailable Continents:")
                        for i, cont in enumerate(continent['Continent'].unique(), 1):
                            print(f"{i}. {cont}")
                        continent_choice = int(input("Select a continent by number: "))
                        area_name = continent['Continent'].unique()[continent_choice - 1]

                        print("\nAvailable Years:")
                        for i, yr in enumerate(continent['Year'].unique(), 1):
                            print(f"{i}. {yr}")
                        year_choice = int(input("Select a year by number: "))
                        year = continent['Year'].unique()[year_choice - 1]

                        continent_instance.growth_calculator(area_name, year)
                    else:
                        print("Invalid choice. Please choose 1 for Region or 2 for Continent.")
                        continue

                    if not analyze_more():
                        break

            elif choice == 5:  # Compare growth rates
                while True:
                    print("\nDo you want to compare growth rates for:")
                    print("1. Region")
                    print("2. Continent")
                    sub_choice = int(input("Choose 1 for Region or 2 for Continent: "))

                    if sub_choice == 1:
                        print("\nAvailable Regions:")
                        for i, reg in enumerate(region['Region'].unique(), 1):
                            print(f"{i}. {reg}")
                        region_choice1 = int(input("Select the first region by number: "))
                        region_choice2 = int(input("Select the second region by number: "))
                        area_name1 = region['Region'].unique()[region_choice1 - 1]
                        area_name2 = region['Region'].unique()[region_choice2 - 1]

                        print("\nAvailable Years:")
                        for i, yr in enumerate(region['Year'].unique(), 1):
                            print(f"{i}. {yr}")
                        year_choice = int(input("Select a year by number: "))
                        year = region['Year'].unique()[year_choice - 1]

                        region_instance.growth_comparison(area_name1, area_name2, year)
                    elif sub_choice == 2:
                        print("\nAvailable Continents:")
                        for i, cont in enumerate(continent['Continent'].unique(), 1):
                            print(f"{i}. {cont}")
                        continent_choice1 = int(input("Select the first continent by number: "))
                        continent_choice2 = int(input("Select the second continent by number: "))
                        area_name1 = continent['Continent'].unique()[continent_choice1 - 1]
                        area_name2 = continent['Continent'].unique()[continent_choice2 - 1]

                        print("\nAvailable Years:")
                        for i, yr in enumerate(continent['Year'].unique(), 1):
                            print(f"{i}. {yr}")
                        year_choice = int(input("Select a year by number: "))
                        year = continent['Year'].unique()[year_choice - 1]

                        continent_instance.growth_comparison(area_name1, area_name2, year)
                    else:
                        print("Invalid choice. Please choose 1 for Region or 2 for Continent.")
                        continue

                    if not analyze_more():
                        break

            elif choice == 6:  # Sort regions or continents by growth rate
                while True:
                    print("\nDo you want to sort by growth rate for:")
                    print("1. Region")
                    print("2. Continent")
                    sub_choice = int(input("Choose 1 for Region or 2 for Continent: "))

                    if sub_choice == 1:
                        print("\nAvailable Years:")
                        for i, yr in enumerate(region['Year'].unique(), 1):
                            print(f"{i}. {yr}")
                        year_choice = int(input("Select a year by number: "))
                        year = region['Year'].unique()[year_choice - 1]

                        region_instance.growth_sort(year)
                    elif sub_choice == 2:
                        print("\nAvailable Years:")
                        for i, yr in enumerate(continent['Year'].unique(), 1):
                            print(f"{i}. {yr}")
                        year_choice = int(input("Select a year by number: "))
                        year = continent['Year'].unique()[year_choice - 1]

                        continent_instance.growth_sort(year)
                    else:
                        print("Invalid choice. Please choose 1 for Region or 2 for Continent.")
                        continue

                    if not analyze_more():
                        break

            else:
                print("Invalid choice. Please select an option from the menu.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

menu(region, continent)

