import csv
import os

# Determine the directory where the script is located
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

# Define the Table class to manage table data with filtering and aggregation methods
class Table:
    def __init__(self, table_name, data):
        self.table_name = table_name
        self.data = data

    def filter(self, condition):
        return [row for row in self.data if condition(row)]

    def aggregate(self, aggregation_function, aggregation_key):
        try:
            values = [float(row[aggregation_key]) for row in self.data if aggregation_key in row and row[aggregation_key]]
            return aggregation_function(values) if values else None
        except ValueError:
            print(f"Error: Non-numeric value encountered in '{aggregation_key}' column.")
            return None

    def __str__(self):
        return f"Table({self.table_name}): {len(self.data)} rows"


# Define the TableDB class to manage multiple tables
class TableDB:
    def __init__(self):
        self.tables = {}

    def insert(self, table_name, data):
        self.tables[table_name] = Table(table_name, data)

    def search(self, table_name):
        return self.tables.get(table_name, None)


# Function to load data from CSV files
def load_csv(file_path):
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        print(f"Error: File not found at path '{file_path}'. Please check the file location.")
        return []
    except Exception as e:
        print(f"An error occurred while reading '{file_path}': {e}")
        return []


# Construct file paths
cities_file = os.path.join(__location__, 'Cities.csv')
countries_file = os.path.join(__location__, 'Countries.csv')

# Load data
cities_data = load_csv(cities_file)
countries_data = load_csv(countries_file)

# Initialize TableDB and insert data
db = TableDB()
db.insert("Cities", cities_data)
db.insert("Countries", countries_data)

# Get cities table
cities_table = db.search("Cities")

if not cities_table:
    print("Error: 'Cities' table not found in the database.")
    exit(1)


# Helper functions for aggregations
def average(values):
    return sum(values) / len(values) if values else None


def minimum(values):
    return min(values) if values else None


def maximum(values):
    return max(values) if values else None


# Print the overall average temperature of all cities
overall_avg_temp = cities_table.aggregate(average, 'temperature')
print("The average temperature of all the cities:", overall_avg_temp)
print()

# Print all cities in Italy
italy_cities = cities_table.filter(lambda x: x['country'] == 'Italy')
italy_city_names = [city['city'] for city in italy_cities]
print("All the cities in Italy:", italy_city_names)
print()

# Average temperature for cities in Italy
italy_avg_temp = Table("Italy_Cities", italy_cities).aggregate(average, 'temperature')
print("Average temperature for cities in Italy:", italy_avg_temp)

# Maximum temperature for cities in Italy
italy_max_temp = Table("Italy_Cities", italy_cities).aggregate(maximum, 'temperature')
print("Maximum temperature for cities in Italy:", italy_max_temp)

# Average temperature for cities in Sweden
sweden_cities = cities_table.filter(lambda x: x['country'] == 'Sweden')
sweden_avg_temp = Table("Sweden_Cities", sweden_cities).aggregate(average, 'temperature')
print("Average temperature for cities in Sweden:", sweden_avg_temp)

# Maximum temperature for cities in Sweden
sweden_max_temp = Table("Sweden_Cities", sweden_cities).aggregate(maximum, 'temperature')
print("Maximum temperature for cities in Sweden:", sweden_max_temp)
print()

# Additional: Min and max latitude for cities in every country
countries = set(city['country'] for city in cities_data)
for country in countries:
    country_cities = cities_table.filter(lambda x: x['country'] == country)
    if country_cities:
        try:
            latitudes = [float(city['latitude']) for city in country_cities if city['latitude']]
            min_latitude = min(latitudes)
            max_latitude = max(latitudes)
            print(f"{country}: Min Latitude = {min_latitude}, Max Latitude = {max_latitude}")
        except ValueError:
            print(f"{country}: Error converting latitude to float.")
    else:
        print(f"{country}: No cities found.")
