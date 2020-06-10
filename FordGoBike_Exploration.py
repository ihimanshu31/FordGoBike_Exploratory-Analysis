#!/usr/bin/env python
# coding: utf-8

# ## Communicate Data Findings
# 
# This project is divided into two major parts.
# 
# - In the first part, you will conduct an **exploratory data analysis** on a dataset of your choosing. 
# - In the second part, you will take your main findings from your exploration and convey them to others through an **explanatory analysis**.
# 
# 
# I will perform an exploratory analysis on data provided by **Ford GoBike**,
# a bike-share system provider.
# 
#      Dataset :https://www.fordgobike.com/system-data
#               https://s3.amazonaws.com/baywheels-data/index.html 
#               i.e.  201904-fordgobike-tripdata.csv.zip
#               
#               Dataset Contain: 239111 Rows & 14 Columns 
#                 i.e     duration_sec               
#                         start_time                
#                         end_time                   
#                         start_station_id           
#                         start_station_name         
#                         start_station_latitude     
#                         start_station_longitude    
#                         end_station_id             
#                         end_station_name           
#                         end_station_latitude       
#                         end_station_longitude      
#                         bike_id                    
#                         user_type                 
#                         bike_share_for_all_trip

# ## Exploratory data Analysis
# 
# **Table of Contents:**
# 
#     1) Introduction
#     2) Data Wrangling for Exploration
#     3) Univariate Exploration
#     4) Bivariate Explorationn
#     5) Multivariate Exploration
#     6) Summary

# In[1]:


#import important packagesabs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import seaborn as sns

import warnings
warnings.filterwarnings('ignore')


# ### Data Wrangling for Exploration

# In[2]:


#import 201904-fordgobike-tripdataset

ford_df= pd.read_csv('201904-fordgobike-tripdata.csv')


# #### Analyze

# In[3]:


ford_df.head()


# In[4]:


#summary
ford_df.info()
ford_df.shape


# In[5]:


ford_df.describe()


# In[6]:


#check duplicte values
ford_df.duplicated().sum()


# In[7]:


#check null values
ford_df.isnull().sum()


# In[8]:



ford_df['user_type'].value_counts()


# #### cleaning

# In[9]:


ford_clean=ford_df.copy()
ford_clean.head(5)


# In[10]:


# convert dates to timestamps
ford_clean.start_time = pd.to_datetime(ford_clean['start_time'])
ford_clean.end_time = pd.to_datetime(ford_clean['end_time'])


# In[11]:


#change start_station_id, end_station_id, bike_id to string
ford_clean.bike_id = (ford_clean['bike_id']).astype(str)
ford_clean.start_station_id = (ford_clean['start_station_id']).astype(str)
ford_clean.end_station_id = (ford_clean['end_station_id']).astype(str)


# In[12]:


ford_clean.user_type= (ford_clean['user_type']) .astype('category')


# In[13]:


ford_clean.info()


# In[14]:


#extract weekday name from start_time
ford_clean['start_time_day']=ford_clean['start_time'].dt.strftime('%a')


# In[15]:


#extract weekday name from start_time
ford_clean['start_time_hour']=ford_clean['start_time'].dt.hour


# In[137]:


ford_clean['duration_min']=ford_clean['duration_sec']/60


# In[138]:


ford_clean.head(2)


# In[18]:


ford_clean['start_time_day'].value_counts()


# ### Exploration (Visualization)

# In[82]:


sns.pairplot(ford_clean, hue='user_type', height=2.5)


# ### Univariate Exploration
#     1) Bikes rides on weekdays
#     2) Hourly rides of the bike
#     3) Trip duration (sec) histogram
#     4) Distribution of User Type

# In[19]:


base_color= sns.color_palette()[0]


# In[20]:


#1) Bikes rides on weekdays
weekday=['Mon',"Tue","Wed","Thu","Fri","Sat","Sun"]
sns.catplot(data=ford_clean, x='start_time_day', kind='count', order=weekday, color=base_color)
plt.title("Bikes rides on weekdays")

plt.xlabel("Weekdays")
plt.ylabel("No. of Bike Trips")


# In[22]:


# 2) Hourly rides of the bike
sns.catplot(data=ford_clean, x='start_time_hour', kind='count',  color=base_color)
plt.title("Hourly rides of the Bikes")

plt.xlabel("Total Hours")
plt.ylabel("No. of Bike Trips")


# In[23]:


#3) Trip duration (sec)
sns.distplot(ford_clean['duration_sec'])
plt.title("Trip Duration In Second")

plt.xlabel("Duration in Sec")


# In[181]:


# 4) Distribution of user type
plt.figure(figsize=(5,5))
a=sns.catplot(data=ford_clean, x='user_type', kind='count',  color=base_color)
a.fig.suptitle("Distribution of user Type")

a.set_axis_labels("User Type", "Count of Users")


# ### Bivariate Exploration
#     1) Weekly usage Trends by user type
#     2) Hourly usage of the bike share system user type
#     3) Bike Rides percentage by user type(Pie chart) : Source:https://pythonspot.com/matplotlib-pie-chart/
#     4) Trip Duration and Start Station
#     5) Trip Duration and End Station
# 
# 

# In[63]:


#1) #weekly usage Trends by user type
weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
a=sns.catplot(data=ford_clean, x='start_time_day', hue='user_type',order=weekday, kind='count', sharey= False,color=base_color)
a.fig.suptitle('Weekly usage Trends by User Type', )

a.set_axis_labels('Weekdays',"No. of bike trips")


# In[64]:


#2) #weekly usage Trends by user type
a=sns.catplot(data=ford_clean, x='start_time_hour', col='user_type', kind='count', sharey= False,color=base_color)
a.fig.suptitle('Hourly usage Trends by User Type' )

a.set_axis_labels('Hours',"No. of bike trips")


# In[91]:


# 3) Bike Rides % by user type
customer = ford_clean.query('user_type == "Customer"')['bike_id'].count()
subscriber = ford_clean.query('user_type == "Subscriber"')['bike_id'].count()

customerP= (customer/ford_clean['bike_id'].count())*100
subscriberP= (subscriber/ford_clean['bike_id'].count())*100

customer, subscriber,customerP,subscriberP

# Data to plot
labels = ['Cistomer', 'Subscriber']
sizes = [customerP,subscriberP]
colors = [ 'coral', 'lightskyblue']
explode = ( 0.2, 0)  # explode 1st slice

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')
plt.show()


# In[115]:


#Trip Duration and Start Station
plt.figure(figsize=(12,5))
sns.lineplot(y="duration_sec", x="start_station_id",data=ford_clean)


# In[118]:


#Trip Duration and End Station
plt.figure(figsize=(12,5))
sns.lineplot(y="duration_sec", x="end_station_id",data=ford_clean)


# #### Multivariate Exploration
#     1) Create faceted scatterplot of the day and time by user type
#         Source: https://seaborn.pydata.org/generated/seaborn.FacetGrid.html
#     
#     2) Duration of bikers acreoss day of week nd hour
#         #Source : https://seaborn.pydata.org/generated/seaborn.pointplot.html
#     
#     3) Showing usage during the weekday for customers and subscribers(Heatmap) 
#         # source: https://seaborn.pydata.org/generated/seaborn.heatmap.html

# In[132]:


# Source: https://seaborn.pydata.org/generated/seaborn.FacetGrid.html
# create faceted scatterplot of the day and time by user type
g = sns.FacetGrid(ford_clean, col="user_type", height=3)
g = g.map(plt.scatter,'start_time_day', "duration_sec",color='r')


# In[160]:


#Source : https://seaborn.pydata.org/generated/seaborn.pointplot.html
#Duration of bikers acreoss day of week nd hour
plt.figure(figsize=(15,7))
a= sns.catplot(x="start_time_hour", y="duration_min",hue='start_time_day',kind="point",data=ford_clean)

a.fig.suptitle('Duration of bikers acreoss day of week nd hour' )

a.set_axis_labels('Duration in minutes',"Days")


# In[178]:


#(Heatmap) Showing usage during the weekday for customers and subscribers
# source: https://seaborn.pydata.org/generated/seaborn.heatmap.html
plt.figure(figsize=(10,7))
plt.suptitle('Showing usage during the weekday for customers and subscribers', fontsize=14)

# Setting the weekday order
ford_clean['start_time_day'] = pd.Categorical(ford_clean['start_time_day'], 
                                                categories=['Mon','Tue','Wed','Thu','Fri','Sat', 'Sun'])


# heatmap for customers
plt.subplot(1, 2, 1)
customer_df = ford_clean.query('user_type == "Customer"').groupby(["start_time_hour", "start_time_day"])["bike_id"].size().reset_index()
customer_df = customer_df.pivot("start_time_hour", "start_time_day", "bike_id")
sns.heatmap(customer_df, cmap="YlGnBu")


# heatmap for subscribers
plt.subplot(1, 2, 2)
subscriber_df = ford_clean.query('user_type == "Subscriber"').groupby(["start_time_hour", "start_time_day"])["bike_id"].size().reset_index()
subscriber_df = subscriber_df.pivot("start_time_hour", "start_time_day", "bike_id")
sns.heatmap(subscriber_df, cmap="YlGnBu")


# **The plot perfectly summarizes the diffrent trends for customers and subscribers**
# 

# ### Summary
#  
#     -TheFord GoBike System is a fantastic (healthy and environmentally friendly)
#     -Customers use the bike sharing system more often on weekends
#     -Subscribers use the bike sharing system mainly on weekdays
