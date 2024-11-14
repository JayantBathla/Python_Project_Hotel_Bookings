#!/usr/bin/env python
# coding: utf-8

# # Hotel Bookings Analysis

# ## BUSINESS PROBLEM
In recent years, City Hotel and Resort Hotel have seen high cancellation rates. Each hotel is now dealing with a number of issues as a result, including fewer revenues and less than ideal hotel room use. Consequently, lowering cancellation rates is both hotels' primary goal in order to increase their efficiency in generating revenue, and for us to offer thorough business advice to address this problem.
The analysis of hotel booking cancellations as well as other factors that have no bearing on their business and yearly revenue generation are the main topics of this report.
# ## Research Areas
1. What are the variables that affect hotel reservation cancellations?

2. How can we make hotel reservations cancellations better?

3. How will hotels be assisted in making pricing and promotional decisions?
# ## Hypothesis
1. More cancellations occur when prices are higher.

2. When there is a longer waiting list, customers tend to cancel more frequently.

3. The majority of clients are coming from offline travel agents to make their reservations.
# In[ ]:





# ### Importing Libraries

# In[39]:


#Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# In[2]:


#loading the dataset
df = pd.read_csv('hotel_bookings.csv')


# ## DATA PRE-PROCESSING AND CLEANING

# In[3]:


# Exploring the data
df


# In[4]:


df.info()


# In[5]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], format="%d/%m/%Y")


# In[6]:


df['reservation_status_date']


# In[7]:


df.describe(include = 'object') #columns with object(string) as values


# In[8]:


# writing all the unique values in all columns with values as object
for col in df.describe(include = 'object'):
    print(col)
    print(df[col].unique())
    


# In[9]:


#Looking for null values
df.isnull().sum()


# In[10]:


# removing columns agent and company because they have a lot of null values that can't be determined and handled as data is 
# 1 Lakh +

df.drop(['company', 'agent'], axis = 1, inplace = True)
df.dropna(inplace = True) # to drop other nulls which is only 490 values that wont affect analysis much


# In[ ]:





# In[11]:


df


# In[12]:


df.describe()


# In[13]:


sns.boxplot(y = df['adr']) # to notice outliers


# In[14]:


df = df[df['adr']<5000]


# In[15]:


df.describe()


# ## Data Visualisations

# In[16]:


#Cancelation Percentage
canceled = round((df['is_canceled'].value_counts()/len(df))*100,2)
canceled


# In[17]:


df['is_canceled'].value_counts().plot(kind = 'bar', figsize = (10,5), edgecolor = 'k')
plt.title('Canceled Status Percentage')

plt.show()


# In[ ]:





# In[18]:


# Looking at the proportions seen in graph it can be noticed and now confirmed with number that proportion of cancelation 
# is more from city hotels


# In[20]:


resort = df[df['hotel'] == 'Resort Hotel']
resort['is_canceled'].value_counts(normalize = True)


# In[21]:


city = df[df['hotel'] == 'City Hotel']
city['is_canceled'].value_counts(normalize = True)


# In[22]:


# how canceling percentage and count depends on tyoe of the hotel
sns.countplot(x = df['hotel'], hue = df['is_canceled'], palette = 'Blues')
plt.title('Cancelation in different hotels')
plt.ylabel('Cancel')
plt.xlabel('Hotel')
# Looking at the proportions seen in graph it can be noticed and now confirmed with number that proportion of cancelation 
# is more from city hotels

The Above bar graph shows the percentage of reservations that are canceled and those that are not. It is obvious that there are still a significant number of reservations that have not been canceled. There are still 37% of clients who canceled their reservation, which has a significant impact on the hotels' earnings.
In comparison to resort hotels, city hotels have more bookings. It's possible that resort hotels are more expensive than those in cities.
# In[23]:


r =resort.groupby('reservation_status_date')[['adr']].mean() #Average daily rate of city hotels
r


# In[24]:


c = city.groupby('reservation_status_date')[['adr']].mean() #Average daily rate of city hotels
c


# In[25]:


plt.figure(figsize = (20,8))
plt.title('Average daily Rates' ,fontsize = 30)
plt.plot(r.index, r['adr'], label = 'Resort hotel')
plt.plot(c.index, c['adr'], label = 'City hotel')
plt.legend()
plt.show()

The line graph above shows that, on certain days, the average daily rate for a city hotel is less than that of a resort hotel, and on other days, it is even less. It goes without saying that weekends and holidays may see a rise in resort hotel rates.
# In[26]:


df['month'] = df['reservation_status_date'].dt.month
sns.set(rc = {'figure.figsize': (12,6)})
sns.countplot(x = 'month', hue = 'is_canceled', data = df)
plt.title('Bookings & Cancelation Status per Month', fontsize = 30)


# In[27]:


cancel = df[df['is_canceled'] ==1]


# In[28]:


#70% of cancellations are from portugal
cancel['country'].value_counts().nlargest(10).plot(kind = 'pie', figsize = (6,6), autopct = '%.2f')
plt.title('Top 10 Countries Based on Cancelations')


# In[29]:


sns.barplot(x='reserved_room_type', y='adr', data=df)
plt.title('Reserved Room Type and Their Corresponding ADR')


# In[ ]:





# In[30]:


m1 = df['market_segment'].value_counts() # Maximum bookings are from online
print(m1)
m1.plot(kind = 'bar', figsize = (12,6))
plt.title('Distribution of bookings on various market segments')


# In[31]:


m2 = cancel['market_segment'].value_counts() # maximum  no. of cancelations also from online mode
print(m2)
m2.plot(kind = 'bar', figsize = (12,6))
plt.title('Distribution of Cancelation of bookings on various market segments')


# In[32]:


# Different types of customers 
df.groupby('customer_type').size().plot(kind = 'pie', autopct = '%.1f')
plt.title('Type of Customer')


# In[33]:


# average adr paid by diff. types of customers
sns.barplot(x='customer_type', y='adr', data=df, palette='Set2', ci=None)
plt.title('Mean ADR by Customer Type')


# In[34]:


# Monthly bookings
monthly_bookings = df.groupby('arrival_date_month').size().sort_index()

# Line plot for monthly bookings
plt.figure(figsize=(12, 6))
sns.lineplot(x=monthly_bookings.index, y=monthly_bookings.values, marker='o', color='teal')
plt.title("Monthly Booking Trends")
plt.xlabel("Month")
plt.ylabel("Number of Bookings")
plt.show()


# In[ ]:





# In[35]:


# How average daily rate(pricing) affects cancellation of bookings


# In[36]:


last_six_months = df[df['reservation_status_date'] >= (df['reservation_status_date'].max() - pd.DateOffset(months=6))]
last_six_months['month_year'] = last_six_months['reservation_status_date'].dt.to_period('M')

adr_trend = last_six_months.groupby(['month_year', 'is_canceled'])['adr'].mean().reset_index()

# Pivot the data for easier plotting
adr_pivot = adr_trend.pivot(index='month_year', columns='is_canceled', values='adr')
adr_pivot.columns = ['Not Canceled', 'Canceled']

# Plot the line chart
plt.figure(figsize=(12, 6))
plt.plot(adr_pivot.index.astype(str), adr_pivot['Not Canceled'], marker='o', label='Not Canceled', color='green')
plt.plot(adr_pivot.index.astype(str), adr_pivot['Canceled'], marker='o', label='Canceled', color='red')
plt.title("Average Daily Rate (ADR) Trend for Canceled vs. Not Canceled Bookings (Last 6 Months)")
plt.xlabel("Month-Year")
plt.ylabel("Average Daily Rate (ADR)")
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.show()

As seen in the graph, reservations are canceled when the average daily rate is higher than when it is not canceled. It clearly proves all the above analysis, that the higher price leads to higher cancellation.
# In[37]:


#Heatmap analysis to understand if there was any other correlation that went un-noticed


# In[38]:


sns.heatmap(df.corr(numeric_only = True))

Created a heatmap to visualize potential hidden relationships and correlations between variables; however, no significant or noteworthy patterns were identified.
# ## Suggestions
1. Cancellation rates rise as the price does. In order to prevent cancellations of reservations, hotels could work on their pricing strategies and try to lower the rates for specific hotels based on locations. They can also provide some discounts to the consumers.

2. In the month of January, hotels can start campaigns or marketing with a reasonable amount to increase their revenue as the cancellation is the highest in this month.

3. They can also increase the quality of their hotels and their services mainly in Portugal to reduce the cancellation rate.