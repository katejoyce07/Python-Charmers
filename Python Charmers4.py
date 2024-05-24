import pandas as pd
taxis = pd.read_csv(
    "C:/Users/KateJoyce/Desktop/Python/2019_Yellow_Taxi_Trip_Data.csv")
taxis.head()

# dropping columns
columns_to_drop = ['vendorid', 'ratecodeid',
                   'pulocationid', 'dolocationid', 'store_and_fwd_flag']
taxis = taxis.drop(columns=columns_to_drop)
taxis.head()

# renaming columns
taxis = taxis.rename(
    columns={
        'tpep_pickup_datetime': 'pickup',
        'tpep_dropoff_datetime': 'dropoff'
    }
)
taxis.columns

# type conversions
taxis.dtypes

# change times to be datetime
taxis[['pickup', 'dropoff']] = taxis[[
    'pickup', 'dropoff']].apply(pd.to_datetime)
taxis.dtypes


# creating new columns
taxis['new_column1'] = 'This is a new column'
taxis = taxis.assign(new_column2=lambda x: 'This is a new column too')
taxis.head(2)

# We can create new columns based on existing columns too.
# Note how 'x' in the lambda function refers to 'taxis' dataframe.

# Trip Time
taxis['trip_time1'] = taxis['dropoff'] - taxis['pickup']
taxis = taxis.assign(trip_time2=lambda x: x.dropoff - x.pickup)
taxis.head(2)

# lets remove these columns before we proceed
more_columns_to_drop = ['new_column1',
                        'new_column2', 'trip_time1', 'trip_time2']
taxis = taxis.drop(columns=more_columns_to_drop)
taxis.head(2)

# Let's calculate the following for each row:
# elapsed time of the trip
# the tip percentage
# the total taxes, tolls, fees, and surcharges
# the average speed of the taxi

taxis = taxis.assign(
    elapsed_time=lambda x: x.dropoff - x.pickup,  # 1
    cost_before_tip=lambda x: x.total_amount - x.tip_amount,
    tip_pct=lambda x: x.tip_amount / x.cost_before_tip,  # 2
    fees=lambda x: x.cost_before_tip - x.fare_amount,  # 3
    avg_speed=lambda x: x.trip_distance.div(
        x.elapsed_time.dt.total_seconds() / 60 / 60
    )  # 4
)

# new columns added to the right
taxis.head(2)

# We used lambda functions to 1) avoid typing taxis repeatedly and 2) be able to access the cost_before_tip and elapsed_time columns in the same method that we create them.
# To create a single new column, we can also use df['new_col'] = <values >.


# Sorting by values

taxis.sort_values(['passenger_count', 'pickup'],
                  ascending=[False, True]).head()

# To pick out the largest/smallest rows, use nlargest() / nsmallest() instead. Looking at the 3 trips with the longest elapsed time, we see some possible data integrity issues:
taxis.nlargest(3, 'elapsed_time')


# Exercise 1 - Read in the meteorite data from the Meteorite_Landings.csv file, rename the mass (g) column to mass, and drop all the latitude and longitude columns. Sort the result by mass in descending order.

meteorites = pd.read_csv(
    "C:/Users/KateJoyce/Desktop/Python/Meteorite_Landings.csv")
meteorites

meteorites = meteorites.rename(
    columns={
        'mass (g)': 'mass',
    }
)
meteorites.columns

columns_to_drop = ['reclat', 'reclong',
                   'GeoLocation']
meteorites = meteorites.drop(columns=columns_to_drop)
meteorites.head()

meteorites.sort_values(['mass'],
                       ascending=[False]).head()


# Working with the index

taxis = taxis.set_index('pickup')
taxis.head(3)

taxis = taxis.sort_index()
taxis['2019-10-23 07:45':'2019-10-23 08']

taxis.loc['2019-10-23 08']

# Resetting the index

taxis = taxis.reset_index()
taxis.head()


# Exercise 2
meteorites = pd.read_csv(
    "C:/Users/KateJoyce/Desktop/Python/Meteorite_Landings.csv")
meteorites

meteorites['year'] = pd.to_datetime(
    meteorites['year'], format='%d/%m/%Y %I:%M:%S %p')

meteorites['year'] = meteorites['year'].dt.year

meteorites['year'].astype(int)

meteorites['fall_before_1970'] = meteorites['year'] < 1970


meteorites.set_index('id')
meteorites.sort_index()

selected_rows = meteorites.loc[10036:10040]

# Display the selected rows
print(selected_rows)
