import snowflake.connector as sf
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
import json

with open("C:/Users/KateJoyce/Desktop/Python/config_sql_workshop.json", 'r') as file:
    config = json.load(file)

user = config['user']
account = config['account']

print(user)


# Load libraries

# gets version
ctx = sf.connect(
    account=account,
    user=user,
    authenticator='externalbrowser'
)

# create cursor object
cur = ctx.cursor()

# execute statement
sql = "SELECT current_version()"
cur.execute(sql)
one_row = cur.fetchone()
print(one_row[0])


# Read data from Snowflake
sql = "SELECT * FROM TIL_PLAYGROUND.PREPPIN_DATA_INPUTS.PD2023_WK01;"
cur.execute(sql)

# fetch result and deliver it as pandas df
df = cur.fetch_pandas_all()
print(df)


# It doesn't have to be just SELECT *, you can run any SQL code
# However for big code blocks include wrap the code in triple single quotes (''')
# this will allow the full string to be captured
# Alternatively you may want to read in a SQL script - more on that later

# set database and schema path
sql = "USE TIL_PLAYGROUND.PREPPIN_DATA_INPUTS;"
cur.execute(sql)

# query table in schema
sql = '''
SELECT
SPLIT_PART(transaction_code, '-',1) as bank,
SUM(value) as total_value
FROM pd2023_wk01
GROUP BY SPLIT_PART(transaction_code, '-',1);
'''
print(sql)

cur.execute(sql)

# fetch result and put in pd
df = cur.fetch_pandas_all()
print(df)


# Write data to Snowflake

write_pandas(conn=ctx, df=df, table_name='PY_TEST_PD2021_WK01',
             database='TIL_PLAYGROUND', schema='TEMP', auto_create_table=True)


# open and read the file as a single buffer
fd = open("C:/Users/KateJoyce/Desktop/Python/example_sql_script.sql", 'r')
sqlFile = fd.read()
fd.close()

print(sqlFile)

cur.execute(sqlFile)

# fetch result and add to df
df = cur.fetch_pandas_all()
print(df)


# Update and Create SQL Scripts
fd = open("C:/Users/KateJoyce/Desktop/Python/example_sql_script.sql", 'r')
sqlFile = fd.read()
fd.close()

# current sql script
print(sqlFile)

# change file contents and view
sqlFile2 = sqlFile.replace('PD2021', 'PD2022')
print(sqlFile2)

# create new sql script file
f = open("C:\/sers/KateJoyce/Desktop/Python/example_sql_script.sql", 'w')
f.write(sqlFile2)
f.close()
