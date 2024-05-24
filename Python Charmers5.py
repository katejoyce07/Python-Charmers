
import numpy as np
from datetime import datetime
import pandas as pd

tsa = pd.read_csv(
    'C:/Users/KateJoyce/Desktop/Python/tsa_passenger_throughput.csv', parse_dates=['Date'])
tsa.head()

# lowercase names
tsa = tsa.rename(columns=lambda x: x.lower().split()[0])
tsa.head()

# Melting
# Melting helps convert our data into long format. Now, we have all the traveler throughput numbers in a single column:

tsa_melted = pd.melt(tsa,  # our dataframe
                     # column, or list of columnd that uniquely identifies a row (can be multiple)
                     id_vars=['date'],
                     var_name='year',  # name for the new column created by melting
                     value_name='travelers'  # name for new column containing values from melted columns
                     )
tsa_melted.sample(5, random_state=1)  # show some random entries

# To convert this into a time series of traveler throughput, we need to replace the year in the date column with the one in the year column. Otherwise, we are marking prior years' numbers with the wrong year.

# 'dt' is the datetime section of the pandas library
# 'strftime' stands for "string format time". It converts datetime objects into a string
# '-%m-%d' access the month and day from the existing date field

tsa_melted = tsa_melted.assign(
    date=lambda x: pd.to_datetime(x.year + x.date.dt.strftime('-%m-%d'))
)

# alternatively you could write
tsa_melted['date'] = pd.to_datetime(
    tsa_melted['year'] + tsa_melted['date'].dt.strftime('-%m-%d'))

tsa_melted.sample(5, random_state=1)


tsa_melted.sort_values('date').tail(3)

# drop nulls
tsa_melted = tsa_melted.dropna()
tsa_melted.sort_values('date').tail(3)


# Pivoting
# Using the melted data, we can pivot the data to compare TSA traveler throughput on specific days across years. Let's look at the first 10 days in March:

# convert column to date format
tsa_melted['date'] = pd.to_datetime(tsa_melted['date'])

# 'copy()' here is ensuring that 'first_10_days' becomes a standalone DataFrame
first_10_days = tsa_melted.loc[(tsa_melted['date'].dt.month == 3) & (
    tsa_melted['date'].dt.day <= 10)].copy()
first_10_days['day_in_march'] = first_10_days['date'].dt.day

# pivot dataset
first_10_days_pivot = pd.pivot(
    first_10_days, index='year', columns='day_in_march', values='travelers')
first_10_days_pivot


# Alternatively these steps can be combined as below
tsa_pivoted = tsa_melted\
    .query('date.dt.month == 3 and date.dt.day <= 10')\
    .assign(day_in_march=lambda x: x.date.dt.day)\
    .pivot(index='year', columns='day_in_march', values='travelers')
tsa_pivoted


# note we currently have two headers, to return to one use '.reset_index()
# the 'day_in_march' column can now be dropped
tsa_pivoted.reset_index()


# Transposing
# The T attribute provides a quick way to flip rows and columns.

tsa_pivoted.T  # or tsa_pivoted.transpose()


# Merging (Joining)¶
# We typically observe changes in air travel around the holidays, so adding information about the dates in the TSA dataset provides more context. The holidays.csv file contains a few major holidays in the United States:

holidays = pd.read_csv("C:/Users/KateJoyce/Desktop/Python/holidays.csv",
                       parse_dates=True, index_col='date')
holidays.loc['2019']

# 'merge()' will join two dataframes, in the form df1.merge(df2, ......)
# 'left_on' & 'right_on' are the columns or list of columns you are joining on,
#   - in this case we use an index so there is a special parameter for that
# 'how' defines the type of join, e.g. 'left','inner',etc.
tsa_melted_holidays = tsa_melted.merge(
    holidays,
    left_on='date',
    right_index=True,
    how='left')

tsa_melted_holidays = tsa_melted_holidays.sort_values('date')
tsa_melted_holidays.head(1000)


tsa_melted_holiday_travel = tsa_melted_holidays.assign(
    holiday=lambda x:
        x.holiday.ffill(limit=1).bfill(limit=2)
)
tsa_melted_holiday_travel.head()

# Note our 'year' column is formatted as a string
tsa_melted_holiday_travel.loc[
    (tsa_melted_holiday_travel['year'] == '2019') &
    ((tsa_melted_holiday_travel['holiday'] == "Thanksgiving") |
     (tsa_melted_holiday_travel['holiday'].str.contains("Christmas")))
]

# Alternatively this can be filtered using 'query()'
tsa_melted_holiday_travel.query(
    'year == "2019" and '
    '(holiday == "Thanksgiving" or holiday.str.contains("Christmas"))'
)


# Aggregations and grouping
# After reshaping and cleaning our data, we can perform aggregations to summarize it in a variety of ways. In this section, we will explore using pivot tables, crosstabs, and group by operations to aggregate the data.

# The pivot_table() function in pandas is similar to pivot(). However, it is more powerful
# it enables you to create summary tables of data by pivoting on one or more columns and
# aggregating values across one or more columns.

pd.pivot_table(
    tsa_melted_holiday_travel,  # the dataframe
    index='year',  # the column(s) to pivot on
    columns='holiday',  # the header columns
    values='travelers',  # the values for our header columns
    aggfunc='sum'  # how we'll aggregrate the data
)

# tsa_melted_holiday_travel.pivot_table(
#     index='year', columns='holiday',
#     values='travelers', aggfunc='sum'
# )


pd.pivot_table(
    tsa_melted_holiday_travel,
    index='year',
    columns='holiday',
    values='travelers',
    aggfunc='sum'
).pct_change(fill_method=None)


pd.set_option('display.float_format', '{:,.0f}'.format)


# If else statements with numpy
# In this next section we'll use the numpy library to create conditional statements, i.e. Ifelse statements, if elseif, IIF()


# np.where(statement, if true, if false)
tsa_melted_holiday_travel['before_pandemic'] = np.where(
    tsa_melted_holiday_travel['date'] < '2020-03-01', 'Y', 'N')
tsa_melted_holiday_travel.head()

# Note you can also nest np.where() statements, e.g.
# np.where(statement, if true, np.where(statement, if true, if false))

# Group Christmas and New Year by removing Day or Eve
tsa_melted_holiday_travel = tsa_melted_holiday_travel.assign(
    holiday=lambda x: np.where(
        x.holiday.str.contains('Christmas|New Year', regex=True),
        x.holiday.str.replace('Day|Eve', '', regex=True).str.strip(),
        x.holiday
    )
)

tsa_melted_holiday_travel.pivot_table(
    index='year',
    columns='holiday',
    values='travelers',
    aggfunc='sum',
    margins=True,  # creates column & row totals
    margins_name='Total'
)

pd.reset_option('display.float_format')


# Exercise 3
# Using the meteorite data from the Meteorite_Landings.csv file, create a pivot table that shows both the number of meteorites and the 95th percentile of meteorite mass for those that were found versus observed falling per year from 2005 through 2009 (inclusive). Hint: Be sure to convert the year column to a number as we did in the previous exercise.

meteorites = pd.read_csv(
    "C:/Users/KateJoyce/Desktop/Python/Meteorite_Landings.csv")
meteorites

meteorites['year'] = pd.to_numeric(meteorites['year'])

meteorites_filtered = meteorites[(
    meteorites['year'] >= 2005) & (meteorites['year'] <= 2009)]

# Pivot the table
pivot_table = meteorites_filtered.pivot_table(
    index='year',
    columns='fall',
    values='mass (g)',
    aggfunc={'mass (g)': ['count', lambda x: x.quantile(0.95)]}
)

# Display the pivot table
print(pivot_table)


# Crosstabs¶
# The pd.crosstab() function provides an easy way to create a frequency table. Here, we count the number of low-, medium-, and high-volume travel days per year, using the pd.cut() function to create three travel volume bins of equal width:


# pd.cut() here is used to segment and sort data values 'travelers' into bins.
tsa_melted_holiday_travel['travel_volume'] = pd.cut(
    tsa_melted_holiday_travel['travelers'], bins=3, labels=['low', 'medium', 'high'])

# pd.crosstab() can now make a quick frequency table by year
pd.crosstab(
    # the bins we created with pd.cut()
    index=tsa_melted_holiday_travel['travel_volume'],
    columns=tsa_melted_holiday_travel['year']  # our column headers
)

# Group by operations
# Rather than perform aggregations, like mean() or describe(), on the full dataset at once, we can perform these calculations per group by first calling groupby():

tsa_melted_holiday_travel.groupby('year').describe(include=np.number)

# Create rank of travelers each year
tsa_melted_holiday_travel['travel_volume_rank'] = tsa_melted_holiday_travel.groupby(
    'year').travelers.rank(ascending=False)

# show top ranks for each year
tsa_melted_holiday_travel.sort_values(['travel_volume_rank', 'year']).head(3)

# Create columns for travellers during the holidays and non-holidays, and converting year to a numeric
tsa_melted_holiday_travel = tsa_melted_holiday_travel.assign(
    holiday_travelers=lambda x: np.where(
        x.holiday.isna(), np.nan, x.travelers),
    non_holiday_travelers=lambda x: np.where(
        x.holiday.isna(), x.travelers, np.nan),
    year=lambda x: pd.to_numeric(x.year)
)

# select_dtypes(include='number') is selecting all numerical data types from our dataframe
tsa_melted_holiday_travel.select_dtypes(
    include='number').groupby('year').agg(['mean', 'std'])


tsa_melted_holiday_travel.assign(
    holiday_travelers=lambda x: np.where(
        x.holiday.isna(), np.nan, x.travelers),
    non_holiday_travelers=lambda x: np.where(
        x.holiday.isna(), x.travelers, np.nan)
).groupby('year').agg({
    'holiday_travelers': ['mean', 'std'],
    'holiday': ['nunique', 'count']
})


# Exercise 4


found_meteorites = meteorites[meteorites['fall'] == 'Found']
falling_meteorites = meteorites[meteorites['fall'] == 'Fell']


found_summary_statistics = found_meteorites['mass (g)'].describe()
falling_summary_statistics = falling_meteorites['mass (g)'].describe()

# Display the summary statistics
print("Summary statistics for found meteorites:")
print(found_summary_statistics)
print("\nSummary statistics for falling meteorites:")
print(falling_summary_statistics)


# 'Mini Project: Preppin' Data 2022: Week 4'

student_df = pd.read_csv("C:/Users/KateJoyce/Desktop/Python/students.csv")
travel_df = pd.read_csv("C:/Users/KateJoyce/Desktop/Python/travel.csv")

print("""Input
""")

print('Students')
print(student_df.head(5))
print(""" 
 
 """)
print('Travel')
print(travel_df.head(5))


# solution - first try answering all quesations first


merged_df = student_df.merge(
    travel_df,
    left_on='id',  # Student DataFrame key column
    right_on='Student ID',  # Travel DataFrame key column
    how='inner'  # Use inner join to include only matching rows
)
print(merged_df)

# Remove any fields you don't need for the challenge
columns_to_drop = ['Parental Contact Name_2', 'Preferred Contact Employer', 'Parental Contact',
                   'pupil first name', 'pupil last name', 'gender', 'Date of Birth', 'Parental Contact Name_1', 'Student ID']
merged_df = merged_df.drop(columns=columns_to_drop)
merged_df.head()

# Change the weekdays from separate columns to one column of weekdays and one of the pupil's travel choice

melted_df = pd.melt(
    merged_df, id_vars=['id'], var_name='weekday', value_name='travel_method')
print(melted_df)


# Define a mapping dictionary to correct spelling errors
correction_spelling = {
    'Aeroplane': ['Aeroplane'],
    'Bicycle': ['Bycycle'],
    'Car': ['Carr'],
    'Dad\'s Shoulders': ['Dad\'s Shoulders'],
    'Helicopter': ['Helicopeter'],
    'Mum\'s Shoulders': ['Mum\'s Shoulders'],
    'Scooter': ['Scootr', 'Scoter'],
    'Walk': ['WAlk', 'Waalk', 'Walkk', 'Wallk']
}


def correct_spelling(method):
    for correct_spelling, misspellings in correction_spelling.items():
        if method in misspellings:
            return correct_spelling
    return method


# Apply the correction function to correct spelling errors in the 'travel_method' column
melted_df['corrected_travel_method'] = melted_df['travel_method'].apply(
    correct_spelling)
print(melted_df)


drop_travel = ['travel_method']
melted_df = melted_df.drop(columns=drop_travel)
melted_df.head()

# Create a Sustainable(non-motorised) vs Non-Sustainable(motorised) data field

sustainability_mapping = [
    'Aeroplane', 'Car', 'Helicopter', 'Van']
melted_df['Sustainable?'] = np.where(melted_df['corrected_travel_method'].isin(
    sustainability_mapping), 'Unsustainable', 'Sustainable')
print(melted_df)


# Total up the number of pupil's travelling by each method of travel
df = melted_df.groupby(['weekday', 'corrected_travel_method', 'Sustainable?']
                       ).size().reset_index(name='Number of Trips')
print(df)

# Work out the % of trips taken by each method of travel each day
df['Trips per day'] = df.groupby('weekday')['Number of Trips'].transform('sum')
df['% of trips per day'] = (
    df['Number of Trips'] / df['Trips per day']).round(2)
print(df)
# Reorder columns
df = df[['Sustainable?', 'corrected_travel_method', 'weekday',
         'Number of Trips', 'Trips per day', '% of trips per day']]

print(df)

# save to csv
df.to_csv('C:/Users/KateJoyce/Desktop/Python/PreppinData20224Output.csv', index=False)
