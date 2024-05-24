# Import libraries
import json
import tableauserverclient as TSC
from tableauhyperapi import TableName
from tableauhyperapi import HyperProcess, Telemetry
from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode, Nullability
import pandas as pd
import pantab

# create dataframe
df = pd.DataFrame([
    ["dog", 4],
    ["cat", 4],
], columns=["animal", "num_of_legs"])

# convert dataframe to hyper file and save locally
pantab.frame_to_hyper(df, "example.hyper", table="animals")

# Note as hyper files can support multiple data sources, table="animals", is here to give a name to each added datasource
# You'll see "animals" when you connect this file to Tableau

# set parameters for no logging and define hyper process
parameters = {"log_config": "", "default_database_version": "1"}
with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU, parameters=parameters) as hyper:

    # create dataframe
    df = pd.DataFrame([
        ["dog", 4],
        ["cat", 4],
    ], columns=["animal", "num_of_legs"])

    # convert dataframe to hyper file and save locally
    pantab.frame_to_hyper(df, "example.hyper",
                          table="animals", hyper_process=hyper)


# CSV File to Hyper


# create df
df = pd.read_csv(
    "C:/Users/KateJoyce/Desktop/Python/2019_Yellow_Taxi_Trip_Data.csv")

pantab.frame_to_hyper(df, "taxi_trips.hyper", table="taxi")


# Hyper to CSV

# read hyper file to dataframe
df = pantab.frame_from_hyper("taxi_trips.hyper", table="taxi")

# save dataframe "df" as csv
df.to_csv('taxi_trips.csv', index=False)


# finding contents of unknown hyper
# Lists the schemas, tables, and columns inside a Hyper file

hyper_file = "taxi_trips.hyper"

# Start Hyper and connect to our Hyper file
with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    with Connection(hyper.endpoint, hyper_file, CreateMode.NONE) as connection:
        # The `connection.catalog` provides us with access to the meta-data we are interested in
        catalog = connection.catalog

        # Iterate over all schemas and print them
        schemas = catalog.get_schema_names()
        print(f"{len(schemas)} schemas:")
        for schema_name in schemas:
            # For each schema, iterate over all tables and print them
            tables = catalog.get_table_names(schema=schema_name)
            print(f" * Schema {schema_name}: {len(tables)} tables")
            for table in tables:
                # For each table, iterate over all columns and print them
                table_definition = catalog.get_table_definition(name=table)
                print(
                    f"  -> Table {table.name}: {len(table_definition.columns)} columns")
                for column in table_definition.columns:
                    nullability = " NOT NULL" if column.nullability == Nullability.NOT_NULLABLE else ""
                    collation = " " + column.collation if column.collation is not None else ""
                    print(
                        f"    -> {column.name} {column.type}{nullability}{collation}")

# Reading and Writing Mulitple Tables
# dataframes to write to hyper


taxi_df = pd.read_csv(
    "C:/Users/KateJoyce/Desktop/Python/2019_Yellow_Taxi_Trip_Data.csv")
hols_df = pd.read_csv("C:/Users/KateJoyce/Desktop/Python/holidays.csv")

# define a dictionary (key pair) of dataframes
dict_of_frames = {
    "taxis": taxi_df,
    "holidays": hols_df
}

pantab.frames_to_hyper(dict_of_frames, "multi.hyper")

# Reading this hyper file will return a dictionary of dataframes
result = pantab.frames_from_hyper("multi.hyper")


# Appending Data to Existing Tables


df = pd.DataFrame([
    ["dog", 4],
    ["cat", 4],
], columns=["animal", "num_of_legs"])

pantab.frame_to_hyper(df, "animals.hyper", table="animals")

new_data = pd.DataFrame([["moose", 4]], columns=["animal", "num_of_legs"])

# append instead of overwriting
pantab.frame_to_hyper(df, "animals.hyper", table="animals", table_mode="a")


# Issuing SQL Queries

# create df
df = pd.read_csv(
    "C:/Users/KateJoyce/Desktop/Python/2019_Yellow_Taxi_Trip_Data.csv")

pantab.frame_to_hyper(df, "taxi_trips.hyper", table="taxi")

# read subset of file
query = """
SELECT 
    passenger_count,
    COUNT(*) as trips,
    SUM(total_amount) as total_fares
FROM taxi
WHERE passenger_count >1
GROUP BY passenger_count
"""
df = pantab.frame_from_hyper_query("taxo_hyper.hyper", query)
print(df)


# Publish a hyper file

with open("C:/Users/KateJoyce/Desktop/Python/config_lesson_8.json", 'r') as file:
    config = json.load(file)

username = config['username']
password = config['password']
server_url = config['server_url']
site_name = config['site_name']

print(username)

# log in
# Username & Password - Tableau Auth
tableau_auth = TSC.TableauAuth(username, password, site_name)
server = TSC.Server(server_url, use_server_version=True)
server.auth.sign_in(tableau_auth)
print('login successful')

# Find project to store
with server.auth.sign_in(tableau_auth):
    # Initialize lists to store project names and IDs
    project_names = []
project_ids = []

# set limit to 1000
req_option = TSC.RequestOptions(pagesize=1000)
all_projects, pagination_item = server.projects.get(req_option)

for project in all_projects:
    project_names.append(project.name)
    project_ids.append(project.id)

proj_df = pd.DataFrame()
proj_df['project_name'] = project_names
proj_df['target_project_id'] = project_ids
print(proj_df)


my_proj = proj_df[proj_df['project_name'].str.contains("Test")]

print(my_proj)

# TO DO
# Enter your project folder id

my_proj_id = ''
hyper_filepath = '../data/taxi_trips.hyper'
display_name = '2019 Taxi Trips'

with server.auth.sign_in(tableau_auth):

    # Use the project id to create new datsource_item
    new_datasource = TSC.DatasourceItem(
        project_id=my_proj_id, name=display_name)

    # publish data source (specified in file_path)
    new_datasource = server.datasources.publish(
        new_datasource, hyper_filepath, 'CreateNew')
