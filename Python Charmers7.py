# List Slicing¶
# List slicing in Python is a powerful and concise way to access a subset of elements from a list.

# Basic Syntax
# The basic syntax for list slicing is list[start:stop:step]
# start(optional) is the index where the slice starts. If omitted, slicing starts from the beginning(index 0).
# stop(optional) is the index where the slice ends, but it's not included in the result. If omitted, slicing goes up to and including the end of the list
# step(optional) is the step size or increment. If omitted, the default value is 1, which means every element in the specified range is included.

# view my list
import pandas as pd
my_list = [1, 2, 3, 4, 5]
print(my_list)

# find the position of an element,
first_item = my_list.index(1)
print(first_item)
# note here python counts start at 0

# find element by position
my_list = [1, 2, 3, 4, 5]
print(my_list[0])

# I can also subset my lists with a certain range of elements
# e.g. the first to the 3rd element
print(my_list[0:3])


# In Python, when you use the slicing syntax my_list[0:3], it means you are asking for a slice of my_list starting from index 0 (inclusive) up to, but not including, index 3.

# This syntax follows the format[start:stop:step], where start is the index where the slice starts, and stop is the index where the slice stops, but is not included in the result

# e.g. the first to the 3rd element
print(my_list[0:3])

# this can be rewritten as,
# all elements stopping before index 3, i.e. the 4th number
print(my_list[:3])

# Similarly this will give all elements starting at index 3, i.e. the 4th number
print(my_list[3:])

# Or using step we can return every other elements
print(my_list[::2])


# Lists becoming dataframe columns
# List can become columns in a dataframe or a dataframe column can become a list.

# Define lists
friends = ["Geetha", "Luca", "Daisy", "Juhan"]
dishes = ["sushi", "burgers", "tacos", "pizza"]

# Create dataframe and assign columns
df = pd.DataFrame()
df['friends'] = friends
df['dishes'] = dishes
print(df)

# columns in the dataframe can be indexed like a list
# i.e. return the first value (element) in this column
print(df['dishes'][0])

# And converted to a list too
friends_dishes = df['dishes'].tolist()
print(friends_dishes)


# List assignment
# We can create list from existing lists, however lists are mutable. This means that they can be changed after they are created. When you assign one list to another(e.g., new_list=given_list), you're not creating a new list; you're creating a reference to the original list. So, any changes made to new_list will also be reflected in given_list.

given_list = [1, 2, 3]
print(given_list)

# Assign given_list to new_list:
new_list = given_list
print(new_list)

new_list[0] = 10
print(new_list)


# However view the previous list, `given_list`:
print(given_list)


# How can we create an independent copy of a list?
# The method copy() creates a new list with the same elements as the original list. In this example, new_list = given_list.copy() creates a separate object new_list that is independent of given_lis

given_list = [1, 2, 3]
new_list = given_list.copy()
new_list[0] = 40
print(given_list)
print(new_list)

# Deep vs Shallow Copy
# It's worth noting that copy() creates a shallow copy. This means it copies the references of the objects contained in the list, not the actual nested objects.

# If you have nested lists or complex objects, you might need a deep copy(using the copy.deepcopy() function) to ensure that nested objects are independently copied as well.


# Adding & removing elements or lists to a list
# Lists are dynamic and can be modified. This section covers how to add and remove elements to/from a list, an essential skill for effective data manipulation in Python

# Add one element at the end of a list:
numbers = [1, 2, 3]
numbers.append(4)
print(numbers)

# Insert the number 2 in position 1:
numbers = [1, 3, 4]
numbers.insert(1, 2)
print(numbers)

# Concatenate two lists:
first_list = [1, 2, 3]
second_list = [4, 5, 6]
third_list = first_list + second_list
print(third_list)

# Add one list at the end of another list:
first_list = [1, 2, 3]
second_list = [4, 5, 6]
first_list.extend(second_list)
print(first_list)

# From the following list, remove all the elements `"ciao"`:
greetings = ["ciao", "ciao", "hello"]
greetings.remove("ciao")
print(greetings)

# Remove the string `"hello"` based on its position:
greetings = ["ciao", "ciao", "hello"]
greetings.pop(2)
print(greetings)

# Remove all elements in a list:
greetings = ["ciao", "ciao", "hello"]
greetings.clear()
print(greetings)


# Mini Project
columns = ['Title', 'Author', 'Year', 'Genre']

data = [
    ['To Kill a Mockingbird', 'Harper Lee', 1960, 'Fiction'],
    ['1984', 'George Orwell', 1949, 'Dystopian'],
    ['The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Fiction']
]

# To Do:

# 1. Data Extraction:
# Extract the 'Year' column from the dataset and store it in a separate list.

years_list = [book[2] for book in data]

print(years_list)
# Use list slicing to create a list of publication years for books published after 1950.
years_list = [book[2] for book in data if book[2] > 1950]

print(years_list)

# 2. Data Modification:
# The genre 'Fiction' is being updated to 'Classic Fiction'. Modify the 'Genre' column to reflect this change.

for book in data:
    if book[3] == 'Fiction':
        book[3] = 'Classic Fiction'

# Print the modified data
for book in data:
    print(book)

# 3. Adding Data
# Add this new book to the dataset
data.append(['Brave New World', 'Aldous Huxley', 1932, 'Dystopian'])
print(data)
