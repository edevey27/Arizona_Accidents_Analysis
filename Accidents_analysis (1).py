#!/usr/bin/env python
# coding: utf-8

# DATA CLEANING
# 
# 1.check the number of columns
# 2.checking for missing values
# 3.checking for duplicate values

# In[273]:


import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Impor the OpenWeatherMap API key
from api_keys import weather_api_key


# In[275]:


#pd.set_option('display.max_columns',None) #not to truncate the columns


# In[277]:


print(os.listdir())


# In[279]:


#file to load--accident
accident_data_to_load = Path("./Resources/accident.csv")

#read accident, person, vehicle data file and store in to Pandas DataFrames

accident_data = pd.read_csv(accident_data_to_load)
accident_data


# In[281]:


accident_data.columns


# In[283]:


#file to load--person
person_data_to_load = Path("./Resources/person.csv")

#read accident, person, vehicle data file and store in to Pandas DataFrames
person_data = pd.read_csv(person_data_to_load)
person_data



# In[285]:


person_data.columns


# In[287]:


accident_data.describe()
person_data.describe()


# In[289]:


accident_data.dtypes
person_data.dtypes


# In[291]:


# check for null values
accident_data.isnull().any()


# In[293]:


#checking for duplicate values--accident

accident_data.duplicated()

#removing duplicate rows

acc_data_duplicates = accident_data.drop_duplicates()
acc_data_duplicates.duplicated().sum()


# In[295]:


# check for null values

person_data.isnull().any()


# In[297]:


person_data.describe()


# In[299]:


#dropping missing value rows
# df = person_data.dropna(inplace=True)
# df


# In[301]:


#to drop missing values of other cols
person_data_null = person_data.dropna(axis=1)

#checking the change
person_data_null.isnull().any()


# In[303]:


person_data_null.describe()


# In[305]:


#checking for duplicate values--person

person_data_null.duplicated()

#removing duplicate rows

person_duplicates = person_data_null.drop_duplicates()

#checking for specific duplicate rows after removal

person_duplicates.duplicated().sum()


# In[307]:


person_duplicates.columns


# In[309]:


#dropping other columns, selecting the necessary col

Dataframe_age = person_duplicates[['AGE','accident_id']]
Dataframe_age


# In[184]:


# Filter the data based on age less than 90
filtered_data = Dataframe_age[Dataframe_age['AGE'] < 90]
filtered_data


# In[208]:


# Group by 'AGE' and count the number of occurrences

age_counts = filtered_data['AGE'].value_counts()
age_counts


# In[313]:


# #filter out the 'AGE' values that have more than one occurrence.
# Filter 'AGE' with more values
age_counts_filtered = age_counts[age_counts >1]

# Create a DataFrame with the filtered 'AGE' counts
filtered_df = age_counts_filtered.reset_index()
filtered_df.columns = ['AGE', 'Count']

# Plot the data using a bar chart
plt.figure(figsize=(10, 6))
plt.bar(filtered_df['AGE'], filtered_df['Count'])
plt.xlabel('age')
plt.ylabel('accidents')
plt.title('Frequency of accidents with age < 90')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.)
plt.savefig("output_data/Fig1.png")
plt.show()


# # Filter the DataFrame for ages less than 90
# filtered_data = Dataframe_age[Dataframe_age['AGE'] < 90]

# # Plot a histogram to show the frequency of accidents for ages less than 90
# #bins=10: This parameter sets the number of bins to 10, meaning the ages will be divided into 10 intervals on the x-axis for the histogram.
# plt.hist(filtered_data['AGE'], bins=10, color='skyblue', edgecolor='black')
# plt.xlabel('Age')
# plt.ylabel('Frequency')
# plt.title('Frequency of Accidents for Ages < 90')
# plt.show()


# In[189]:


#dropping other columns, selecting the necessary col--acc

Dataframe_weather_tway = acc_data_duplicates[['weather_lit','TWAY_ID','lgt_cond_lit','YEAR']]
Dataframe_weather_tway


# In[190]:


# 'acc_data_duplicates' contains data:
#Dataframe_weather_tway = acc_data_duplicates[['weather_lit','TWAY_ID','lgt_cond_lit','YEAR']]

Dataframe_weather_tway = acc_data_duplicates[['LATITUDE','accident_id']]

# Group by latitude and aggregate the accident counts--group the data lat col
#Use an aggregate function 'count' to summarize the accident data within each latitude group.

accidents_by_latitude = Dataframe_weather_tway.groupby('LATITUDE').agg({'accident_id': 'count'}).reset_index()

# Plot the aggregated data to view the relationship between accidents and latitude.
accidents_by_latitude.plot(x='LATITUDE',
                           y='accident_id', 
                           kind='scatter', 
                           xlabel='Latitude', 
                           ylabel='Number of Accidents', title='Accidents by Latitude')
plt.savefig("output_data/Fig2.png")


# In[193]:


tway_counts = acc_data_duplicates['TWAY_ID'].value_counts()
tway_counts


# In[319]:


#filter out the 'TWAY_ID' values that have more than one occurrence.
# Filter 'TWAY_ID' with more values
tway_counts_filtered = tway_counts[tway_counts >9]

# Create a DataFrame with the filtered 'TWAY_ID' counts
filtered_df = tway_counts_filtered.reset_index()
filtered_df.columns = ['TWAY_ID', 'Count']

# Plot the data using a bar chart
plt.figure(figsize=(12, 4))
plt.bar(filtered_df['TWAY_ID'], filtered_df['Count'])
plt.xlabel('TWAY_ID')
plt.ylabel('Accidents')
plt.title('Number of Accidents with TWAY_ID')
plt.xticks(rotation=85)
plt.grid(axis='y', linestyle='--', alpha=0.2)
plt.savefig("output_data/Fig3.png",bbox_inches='tight')
plt.show()


# In[197]:


#pie chat showing distribution of weather

count = acc_data_duplicates['YEAR'].value_counts()
plt.pie(count.values, labels = count.index, autopct = '%1.1f%%')
plt.title('distribution of accidents')
plt.savefig("output_data/Fig4.png")
plt.show()



# In[311]:


#filter the col year and weather_lit

filtered_df= acc_data_duplicates[['YEAR','weather_lit']]
filtered_df

#group the data by year and weather_lit to get counts
grouped_data = filtered_df.groupby(['YEAR', 'weather_lit']).size()

grouped_data.plot(kind='bar', figsize=(12, 4))
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Distribution of accidents over the Years in different weather')
plt.savefig("output_data/Fig4.png",bbox_inches='tight')
plt.show()





# In[321]:


# # Group data by 'lgt_cond_lit' and 'YEAR' to count the number of accidents per traffic way per year
# accidents_by_tway_year = acc_data_duplicates.groupby(['lgt_cond_lit', 'YEAR']).size().reset_index(name='accident_count')

# # Create a pivot table to reshape the data for plotting
# pivot_table = accidents_by_tway_year.pivot(index='YEAR', columns='lgt_cond_lit', values='accident_count')

# # Plot a stacked bar chart showing the number of accidents in different traffic ways over the years
# pivot_table.plot(kind='bar', figsize=(12, 6))  

# # Set labels and title for the chart
# plt.xlabel('Year')
# plt.ylabel('Number of Accidents')
# plt.title('Number of Accidents in Different conditions Over the Years')
# plt.legend(title='conditions', loc='upper right')
# plt.savefig("output_data/Fig5.png")
# # Display the chart
# plt.show()



filtered_df= acc_data_duplicates[['lgt_cond_lit','YEAR']]
filtered_df


# Group the data by "YEAR" and "lgt_cond_lit" and count the number of accidents
grouped_data = filtered_df.groupby(['YEAR', 'lgt_cond_lit']).size()

# Plot a bar chart
grouped_data.unstack().plot(kind='bar', stacked=True, figsize=(12, 4))
plt.xlabel('Year')
plt.ylabel('Number of Accidents')
plt.title('Number of Accidents in Different Light Conditions by Year')
plt.legend(title='Light Condition')
plt.savefig("output_data/Fig5.png",bbox_inches='tight')
plt.show()


# In[ ]:




