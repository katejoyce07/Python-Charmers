
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

# Q1
airline = pd.read_csv(
    "C:/Users/KateJoyce/Desktop/Python/T100_MARKET_ALL_CARRIER.zip")
airline.head()

airline = airline.rename(columns=lambda x: x.lower().split()[0])
airline.head()

# Q2
airline.columns

# Q3
airline.unique_carrier_name.nunique()

# Q4
airline.query('origin_country_name == "United Kingdom" and dest_country_name == "United States"'
              )[['freight', 'mail', 'passengers']].sum()

# Q5
airline[['unique_carrier_name', 'origin', 'dest', 'distance']].drop_duplicates()\
    .groupby('unique_carrier_name').distance.median().nlargest(5)

# Q6
airline.assign(cargo=lambda x: x.mail + x.freight)\
    .groupby('unique_carrier_name')[['cargo', 'distance']]\
    .agg(dict(cargo='sum', distance='mean')).nlargest(10, 'cargo')

# Q7
top_10_by_passengers = airline\
    .query('origin_country_name == "United States" and dest_country_name != "United States"')\
    .groupby('unique_carrier_name').passengers.sum().nlargest(10)
top_10_by_passengers

# Q8
airline.query('origin_country_name == "United States" and dest_country_name != "United States"')\
    .groupby(['unique_carrier_name', 'dest_country_name']).passengers.sum()\
    .groupby(level=0, group_keys=False).nlargest(1)[top_10_by_passengers.index]

# Q9
airline.query(
    'origin_country_name.isin(["Canada", "Dominican Republic", "Germany", "Mexico", "United Kingdom", "United States"])'
    ' and dest_country_name.isin(["Canada", "Dominican Republic", "Germany", "Mexico", "United Kingdom", "United States"])'
    f' and dest_country_name != origin_country_name and unique_carrier_name.isin({top_10_by_passengers.index.to_list()})'
).groupby('unique_carrier_name').passengers.sum().sort_values(ascending=False)


# Q10
top_route = airline.sort_values(['origin_city_name', 'dest_city_name']).assign(
    route=lambda x:
        x[['origin_city_name', 'dest_city_name']].min(axis=1)
        + '-'
        + x[['origin_city_name', 'dest_city_name']].max(axis=1)
).groupby('route').passengers.sum().nlargest(1)
top_route

# Q11
top_3 = airline.sort_values(['origin_city_name', 'dest_city_name']).assign(
    route=lambda x:
        x[['origin_city_name', 'dest_city_name']].min(axis=1)
        + '-'
        + x[['origin_city_name', 'dest_city_name']].max(axis=1)
).query(
    'route == "Chicago, IL-New York, NY"'
).groupby('unique_carrier_name').passengers.sum().div(top_route.iloc[0]).nlargest(3)
top_3

# Q12
international_passenger_travel = airline.query(
    'origin_country_name != dest_country_name and `class` == "F"'
).assign(
    international_country=lambda x: np.where(
        x.origin_country_name != 'United States', x.origin_country_name, x.dest_country_name)
).groupby('international_country').passengers.sum()

international_travel_pct = (
    international_passenger_travel / international_passenger_travel.sum()).nlargest(5)
international_travel_pct

# Q13
international_travel = airline.query(
    'origin_country_name != dest_country_name and `class` == "F"'
).assign(
    us_city=lambda x: np.where(
        x.origin_country_name == 'United States', x.origin_city_name, x.dest_city_name),
    international_country=lambda x: np.where(
        x.origin_country_name != 'United States', x.origin_country_name, x.dest_country_name)
)

pd.crosstab(
    index=international_travel.unique_carrier_name, columns=international_travel.international_country,
    values=international_travel.passengers, aggfunc='sum', normalize='index'
).loc[top_3.index, international_travel_pct.index]


# Q15
international_travel = airline.query(
    'origin_country_name != dest_country_name and `class` == "F"'
).assign(
    us_city=lambda x: np.where(
        x.origin_country_name == 'United States', x.origin_city_name, x.dest_city_name),
    international_country=lambda x: np.where(
        x.origin_country_name != 'United States', x.origin_country_name, x.dest_country_name)
)

international_travel_pivot = international_travel.pivot_table(
    index='us_city', columns='international_country',
    values='passengers', aggfunc='sum', margins=True
).sort_values('All', ascending=False, axis=1).sort_values('All', ascending=False)

normalized_international_travel = (
    international_travel_pivot / international_travel_pivot.loc['All']).drop('All').drop(columns='All')
pct_of_passengers_country = normalized_international_travel.iloc[:10, :15].sort_index(
).sort_index(axis=1)
pct_of_passengers_country

# Q16

fig, axes = plt.subplots(figsize=(14, 8))

sns.heatmap(pct_of_passengers_country, cmap='Blues',
            annot=True, fmt='.1%', ax=axes)
axes.set(
    title='Percentage of travel to/from foreign countries via the top 10 US cities for international passenger travel.',
    xlabel='International country', ylabel='US city'
)
