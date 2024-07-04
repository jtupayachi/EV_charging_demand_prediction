"""_summary_: This Script read the data and creates the unique days between 
the initial day of charge and last, timezone and zipcode so data can be downloaded.

It seems wunderground.com uses local time
"""

import pandas as pd
import ast
# Read the data into a pandas DataFrame
df = pd.read_csv('EV Dataset/California EVChargingStationUsage.csv', low_memory=False)[['Start Date', 'Start Time Zone', 'End Date', 'End Time Zone','City', 'Postal Code']]

# Convert 'Start Date' and 'End Date' to datetime
df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')

# Generate list of dates between Start Date and End Date for each row, containing only the date portion
df['Date List'] = df.apply(lambda row: [d.date() for d in pd.date_range(start=row['Start Date'].date(), end=row['End Date'].date())], axis=1)

# Create a temporary column for the string representation of 'Date List'
df['Date List Str'] = df['Date List'].apply(lambda x: str(x))

# Drop duplicates using the temporary column
df.drop_duplicates(subset=['Postal Code', 'Date List Str','City'], inplace=True)

# Drop the temporary column
df.drop(columns=['Date List Str'], inplace=True)
df.reset_index(inplace=True,drop=True)

df=df[['Postal Code','Date List','City']]
df = df.explode('Date List')


df.drop_duplicates(subset=['Postal Code','Date List','City'], inplace=True)
df.reset_index(inplace=True,drop=True)






# Assuming 'Date List' is already in date string format, convert to list of strings
df['Date List'] = df['Date List'].apply(lambda x: [x])


# # Convert 'Date List' column from string to list of strings
# df['Date List'] = df['Date List'].apply(ast.literal_eval)


df.to_csv('simplified/california.csv',index=False)


print(df)