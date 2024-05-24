# What types of Python Loops are there?¶
# There is a for loop and a while loop. We'll also go through list comprehensions, as a "Pythonic" powerful shortcut for operating on all the members of a list in a single line of code.

# The for statement*
# A "for" loop in Python allows you to go through each item in a sequence, one at a time. This allows you to "iterate" through an "iterable", such as a Python list, and perform operations on each item one at a time.

# The simplest example is to step through the items in a list: d.

# In the below example, the for loop will step through each item in my_list, assign the element to a local variable ("x"),
# and execute the block of code below it to print out x

import json
import tableauserverclient as TSC
import pandas as pd
my_list = [10, 20, 30, 40, 50, 60]
for x in my_list:  # <--- x is a variable, who's scope is limited to the for loop. x can be named anything you'd like
    print(x)


# The range function
# range() will create a list from 0 to one before the number provided
for i in range(8):
    print(i)

# range and len
my_list = [10, 20, 30, 40, 50, 60]

for i in range(len(my_list)):
    print(i, my_list[i])


my_list = [10, 20, 30, 40, 50, 60]
results = []

for i in range(len(my_list)):
    results.append(i)

print(results)


# and then I can take these lists and create a Dataframe

# Create dataframe and assign columns
df = pd.DataFrame()
df['my_list'] = my_list
df['results'] = results
print(df)


# Enumerate
# You can achieve the same effect as above by using the enumerate() function, to get two values each step through the loop.

# the enumerate function will return two values each time the loop statement is run:
# "indx" will be the current index value, and "val" will be the current element of my_list
for indx, val in enumerate(my_list):
    print(indx, val)

# Loop through the characters in a string
# You can also loop through all characters in a string of text in order

s = "One at a time"
for character in s:
    print(character)


# A Python Dictionary
# What's a dictionary?¶
# A dictionary in Python is a collection of key-value pairs. It's a mutable data type, meaning it can be changed after it's created. Each key in a dictionary is unique and is used to access its corresponding value.

# creating a dictionary
person = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Acessing Elements
print("Name", person["name"])
print("Age", person["age"])

# Adding a new key-value pair
person["email"] = "john@example.com"
print(person)

# Updating an existing key
person["age"] = 31
print(person)

# Removing a key value pair
del person["city"]
print(person)


# Looping throug a dictionary
# keys()

my_dict = {'AAPL': 100, 'MSFT': 200, 'GOOG': 300, 'CSCO': 400}

for key in my_dict.keys():
    print(key)

# items()

my_dict = {'AAPL': 100, 'MSFT': 200, 'GOOG': 300, 'CSCO': 400}

for key, value in my_dict.items():
    print('Key= ' + key + ', Value= ' + str(value))


# The while loop
# Though not used as frequently as the for loop, the while loop allows you to execute a block of code until a certain condition is met. If you don't know before-hand how many times to iterate, then a while loop may be appropriate

# A while loop in Python repeatedly executes a block of code as long as a given condition is true.

# Initialize a counter varible

counter = 0

# start while loop
while counter < 5:
    print("Counter is", counter)
    # increment the counter
    counter += 1

print("Loop Finished")

# Note: counter += 1 is the same as:
# counter = counter + 1


# List Comprehensions (somewhat advanced)¶
# List comprehensions provide a convenient shorthand to create a new list from an existing list by performing an operation on each member of the original list. The general syntax for a simple list_comprehension looks like:

# [python_expression_that_can_reference_var_name for var_name in list_name]

# Below is an example of using a list comprehension to create a list of the squares of an original list.

my_list = [1, 2, 5, 7, 12, 17]
[x*x for x in my_list]


# Mini Project

# pip install tableauserverclient via terminal, if this package is not found

# If you don't have a Tableau Cloud account you can sign up for free here:
# Tableau Developer Programme: https://www.tableau.com/en-gb/developer

# There are two ways to authenticate, which one you choose will depend on how you login to your Tableau Server:
# - Username & Password
# - Personal Access Token

# However we do not want to share these details with the world,
# so we will read these values from a local file, "config".
# this means you can share this script without comprimising your access.


with open('C:/Users/KateJoyce/Desktop/Python/config_lesson_8.json', 'r') as file:
    config = json.load(file)

username = config['username']
password = config['password']
server_url = config['server_url']
site_name = config['site_name']

print(username)

# Username & Password - Tableau Auth
tableau_auth = TSC.TableauAuth(username, password, site_name)
server = TSC.Server(server_url, use_server_version=True)
server.auth.sign_in(tableau_auth)
print('login successful')

with server.auth.sign_in(tableau_auth):
    print('Logged into server')
    all_workbooks, pagination_item = server.workbooks.get()

# server.workbooks.get() retrieves all the workbooks from the Tableau server

# it returns two items:
# - all_workbooks - a list of all workbooks on the server
# - pagination_item - give details like the total number of workbooks

for workbook in all_workbooks:
    print(workbook)
    break


# ISSUE COME BACK
