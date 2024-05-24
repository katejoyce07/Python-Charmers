# APIS
# RandomUser API: Calling an API via a Python Package
# Some packages in python act as interfaces for APIs, so you

# Import python library
import json
import requests
import pandas as pd
from randomuser import RandomUser

# load a random user object
r = RandomUser()

# Using "Getter" methods (i.e. get_ ...) we can obtain data from the API call results
print(r.get_full_name())
print(r.get_gender())
print(r.get_dob())

print(" ")
print(r.get_street())
print(r.get_city())
print(r.get_state())
print(r.get_zipcode())


# Using generate_users() function, we get a list of random 10 users.

# load a random user object
r = RandomUser()

list_of_users = r.generate_users(10)
print(list_of_users)

# However we can't apply a "Getter" method to a list
names = list_of_users.get_full_name()

for user in list_of_users:
    print(user.get_full_name())


# Exercise 1


# load a random user object
r = RandomUser()

# initialise lists
name = []
gender = []
city = []
state = []
email = []
dob = []
picture = []

# loop through a list of 10 users and append results to lists
for user in r.generate_users(10):
    name.append(user.get_full_name())
    gender.append(user.get_gender())
    city.append(user.get_city())
    state.append(user.get_state())
    email.append(user.get_email())
    dob.append(user.get_dob())
    picture.append(user.get_picture())

# create dataframe and set lists as columns
df = pd.DataFrame()
df['name'] = name
df['gender'] = gender
df['city'] = city
df['state'] = state
df['email'] = email
df['dob'] = dob
df['picture'] = picture

print(df)


# quicker way of doing this


r = RandomUser()

users = []

# loop through list of 10 users and append results to dictionary
for users in r.generate_users(10):
    users.append(
        {"Name": user.get_full_name(),
         "Gender": user.get_gender(),
         "City": user.get_city(),
         "State": user.get_state(),
         "Email": user.get_email(),
         "DOB": user.get_dob(),
         "Picture": user.get_picture()
         })

# convert dictonary to df
df = pd.DataFrame(users)
print(df)


# Fruitvice API: Calling an API via a website


data = requests.get("https://fruityvice.com/api/fruit/all")

# printing this returns <Response [200]> not the data...
print(data)

# check the methods available for this object
print(dir(data))

# the json() method will return the json data contained in the response
results = data.json()

# We will convert our json data into pandas data frame.
df = pd.DataFrame(results)
print(df.head())

# Alternatively, you can use the ".text" method
# and load the data using the "json.loads()" function. e.g.
# results = json.loads(data.text)

# flatten data - nested json
df2 = pd.json_normalize(results)
print(df2.head())


# Mini Project

with open("C:/Users/KateJoyce/Desktop/Python/config_lesson_9.json", 'r') as file:
    config = json.load(file)

api_key = config['met_office_api_key']

print(api_key)

# add key to base url

api_call = 'http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/3840?res=3hourly&key=' + api_key
data = requests.get(api_call)

response = requests.get(api_call)

# checking the method of the object there is a "json" method we can call
print(dir(response))

# viewing this data we can see its very nested
json_data = response.json()
print(json_data)

# The first section explains the column headers and meta data
# The next section contains the recorded weather values


# For column headers we access via querying the nested json headers
column_json = json_data['SiteRep']['Wx']['Param']
column_df = pd.json_normalize(column_json)
print(column_df)

meta_json = json_data['SiteRep']['DV']
meta_df = pd.json_normalize(meta_json)
print(meta_df)

# accessing weather data
weather_data = json_data['SiteRep']['DV']['Location']['Period']
df = pd.json_normalize(weather_data)
print(df.head())

# convert list elements to rows
df2 = df.explode('Rep')
print(df2.head())

# expand to columns
expanded_rep = df2['Rep'].apply(pd.Series)

weather_df = df2[['type', 'value']].join(expanded_rep)
print(weather_df.head())


# Bringing this all together we can output three-hourly five-day forecast for temperatures at DUNKESWELL AERODROME
# Note "F" here is the "feels like temperature" in Celsius
# And "$" is the time in minutes, i.e. 360 is 6 am

temp_forecast_df = weather_df[['type', 'value', 'F', '$']].copy()
temp_forecast_df['location_name'] = meta_df['Location.name'][0]
temp_forecast_df['reading_type'] = meta_df['type'][0]

print(temp_forecast_df)


# Exercise: Weather Observations

# locations of weather stations in the Shetlands
location_ids = ['3002', '3005', '3008', '3014']

# Selecting a weather station
location_id = location_ids[0]

# building an API call
api_call = 'http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/' + \
    location_id + '?res=hourly&key=' + api_key
data = requests.get(api_call)
print(data)

# TO DO

# Create a Loop that will call this API for each of the four locations
# Prep the json data returned into a dataframe containing:
#  - location name
#  - dataDate
#  - lat & lon
#  - hour
#  - Temperature

# If no data is returned from the API call replace the location with another weather station from the sitelist call above
