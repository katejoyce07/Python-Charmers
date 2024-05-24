# Python Charmners - 3

import requests
import pandas as pd

meteorites = pd.read_csv(
    'C:/Users/KateJoyce/Desktop/Python/Meteorite_Landings.csv')
meteorites

meteorites.name

meteorites.columns

meteorites.index

meteorites.shape

meteorites.dtypes


# WHAT DOES THE DATA LOOK LIKE?
meteorites.head()

# check the last few rows
meteorites.tail()

# filtering with boolean mask
(meteorites['mass (g)'] > 50) & (meteorites.fall == 'Found')

[(meteorites['mass (g)'] > 1e6) & (meteorites.fall == 'Fell')]

meteorites = pd.read_csv(
    'C:/Users/KateJoyce/Desktop/Python/Meteorite_Landings.csv')

meteorites.query("`mass (g)` > 1e6 and fall == 'Fell'")


response = requests.get(
    'https://data.nasa.gov/resource/gh4g-9sfh.json',
    params={'$limit': 50_000}
)

if response.ok:
    payload = response.json()
    print("success")
else:
    print(
        f'Request was not successful and returned code: {response.status_code}.')
    payload = None

df = pd.DataFrame(payload)
df.head(3)

# get info about the dataframe
meteorites.info()


# Excercise 1
package_name = pd.read_csv(
    "C:/Users/KateJoyce/Desktop/Python/2019_Yellow_Taxi_Trip_Data.csv", nrows=5)
package_name.head()
print(package_name)


# Exercise 2
package_name = pd.read_csv(
    "C:/Users/KateJoyce/Desktop/Python/2019_Yellow_Taxi_Trip_Data.csv", nrows=5)
print("Number of rows and columns:", package_name.shape)


# selecting columns
meteorites.name

# multiple columns
meteorites[['name', 'mass (g)']]

# selecting rows
meteorites[100:104]

# indexing
meteorites.iloc[100:104, [0, 3, 4, 6]]

# Calculating summary statistics
meteorites = pd.read_csv(
    '"C:/Users/KateJoyce/Desktop/Python/Meteorite_Landings.csv"')
meteorites

# How many of the meteorites were found versus observed falling?

meteorites.fall.value_counts()

# What was the mass of the average meterorite?
meteorites['mass (g)'].mean()

# median is better
meteorites['mass (g)'].median()

# what was the heaviest meteorite?
meteorites['mass (g)'].max()

# lets extract info
meteorites.loc[meteorites['mass (g)'].idxmax()]

# How many different types of meteorite classes are represented in this dataset?
meteorites.recclass.nunique()

# Get some summary statistics on the data itself
meteorites.describe(include='all')

# Exercise 3 - listing specific columns in summary stats
taxis = pd.read_csv(
    "C:/Users/KateJoyce/Desktop/Python/2019_Yellow_Taxi_Trip_Data.csv")
taxis

taxis[['fare_amount', 'tip_amount', 'tolls_amount', 'total_amount']].describe()

# Exercise 4
taxis = pd.read_csv(
    "C:/Users/KateJoyce/Desktop/Python/2019_Yellow_Taxi_Trip_Data.csv")
taxis

max_trip_distance = taxis['trip_distance'].max()
print("Maximum Trip Distance:", max_trip_distance)

longest_trip_df = taxis[taxis['trip_distance'] == max_trip_distance]

# Extract required columns
fare_amount = longest_trip_df['fare_amount'].iloc[0]
tip_amount = longest_trip_df['tip_amount'].iloc[0]
tolls_amount = longest_trip_df['tolls_amount'].iloc[0]
total_amount = longest_trip_df['total_amount'].iloc[0]

print("Fare Amount:", fare_amount)
print("Tip Amount:", tip_amount)
print("Tolls Amount:", tolls_amount)
print("Total Amount:", total_amount)
