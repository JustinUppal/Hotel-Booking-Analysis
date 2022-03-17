import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import argparse as argparse

# Questions to answer

# What does the data suggest regarding how bookings differ by platform and region?
# Where are we seeing the most growth? 
# What other data or information would we request to gain additional insight? 


df10 = pd.read_excel('2017_ExpediaDataset.xlsx', index_col=0).reset_index(drop=True)
df9 = pd.read_excel('2016_ExpediaDataset.xlsx', index_col=0).reset_index(drop=True)

df = pd.concat((df9, df10), ignore_index=True)

df.head()

# I have some ideas
# plot by super-region: How many are from desktop and how many from mobile,
# the booking-group window (histogram), net-order histogram, and 
# then lastly a net-gross booking histogram.


# I'm checking to see the Super Regions that are all there.
set(df['Super Region'])

# so I see there are some empty values, going to look for more info here

df[df['Super Region'].isna()]

# It seems like that empty region is entirely in the United States because of 'Country Name'. Lets make sure

set(df[df['Super Region'].isna()]['Country Name'])

# Okay, so all the empty rows for Super Region are actually in the US.
# We can rename the empty Super Regions to US then.

df.loc[df['Super Region'].isna(), 'Super Region'] = 'US'

# Lets make sure it all works here.
set(df['Super Region'])

# Lets see how many desktop orders we have total.
df[df['Mobile Indicator Name'] == 'Desktop'].shape[0]

# Now lets check mobile.
df[df['Mobile Indicator Name'] == 'Mobile'].shape[0]

# I want to look at Net Orders now.
# This is total number of (hotel bookings made - the number of bookings cancelled)
df['Net Orders'].describe()

# There average is 47 but somehow, there is a -50 value and there is also a 991 value.
# We need the clean the data for sure.


# First, I'm just going to see what the top 10% of all values are.
df['Net Orders'].quantile(.9)

# 28 is pretty normal given that the mean is 47.
# Lets check the top 5%
df['Net Orders'].quantile(.95)

# Again, 58 is pretty normal given that the mean is 47.
# Lets check top 1%.
df['Net Orders'].quantile(.99)

# Whoa, big jump here.
# Let's delete everything that is above this value. This is skewing our data

df.loc[df['Net Orders'] >= df['Net Orders'].quantile(.99), 'Net Orders'] = 0

# Now, lets check the bottom 1% to find our how we have -50
df['Net Orders'].quantile(.01)

# Okay lets cut out everything below this value. It is skewing our data

df.loc[df['Net Orders'] < df['Net Orders'].quantile(.01), 'Net Orders'] = 0

# Now lets check it out.


df['Net Orders'].describe()

df['Net Gross Booking Value USD'].describe()

# The data definitely needs to be cleaned. How is there negative dollars in the minimum
df['Net Gross Booking Value USD'].quantile(.99)

df.loc[df['Net Gross Booking Value USD'] >= df['Net Gross Booking Value USD'].quantile(
    .99), 'Net Gross Booking Value USD'] = 0

df.loc[df['Net Gross Booking Value USD'] < df['Net Gross Booking Value USD'].quantile(
    .05), 'Net Gross Booking Value USD'] = 0

df['Net Gross Booking Value USD'].describe()

# Visualizing here. # This is mostly just to see the data.
plt.hist(df['Net Gross Booking Value USD'])

# building a series to show Super Regions with the most mobile orders
df.groupby(['Platform Type Name', 'Super Region'])['Net Gross Booking Value USD'].sum().sort_values(ascending=False)

# Now for times of Growth

# We need just another column that is just year of each week

set(df['Week'])

# We need to make a column that is just year of each week. This week by week stuff is kind of useless.
df['Year'] = df['Week'].str[:4]

# Checking columns now to make sure 'Year' is there.


# Creating a dataframe that is the all of the information for the year 2016
df[df['Year'] == "2016"].groupby(['Platform Type Name', 'Super Region', 'Year'])['Net Gross Booking Value USD'].sum()
df2 = df[df['Year'] == "2016"].groupby(['Platform Type Name', 'Super Region'])[
    'Net Gross Booking Value USD'].sum().to_frame(name='2016')

# Doing the same thing for 2017
df[df['Year'] == "2017"].groupby(['Platform Type Name', 'Super Region'])['Net Gross Booking Value USD'].sum()

df[df['Year'] == "2017"].groupby(['Platform Type Name', 'Super Region'])['Net Gross Booking Value USD'].sum()

df2['2017'] = df[df['Year'] == "2017"].groupby(['Platform Type Name', 'Super Region'])[
    'Net Gross Booking Value USD'].sum()

# now I have a second dataframe and this can show growth.


df2['Percent_Change'] = (df2['2017'] / df2['2016'] - 1) * 100

# Question 3: What users in what regions like certain platforms.

# Mobile App Usage Increased by 147% and Mobile Web Usage increased 64% in APAC
# App Usage in general is up big, but specifically in Latam, EMEA and APAC.
# Most Growth is APAC Mobile App and LATAM Mobile 


# Desktop bookings most popular by quite a bit, Mobile Web/App trail each other.
df.groupby(['Platform Type Name'])['Net Gross Booking Value USD'].sum().sort_values(ascending=False)

# Most business in US/APAC/EMEA, LATAM trails far behind.


df.groupby(['Super Region'])['Net Gross Booking Value USD'].sum().sort_values(ascending=False)

# Just from these two tables ,we have the most room for growth by booking people in US/APAC/EMEA on their mobile
# devices.


# QUESTION 4
# We need to consider population size.
# LATAM is so far behind?
# LATAM is missing many countries in the dataset, maybe this is why it is so far behind.


# Even if LATAM is the same population as EMEA, then the demographics of who we are trying to sell to might be
# different. We need to consider demographics of who we are targeting. Retirees? College students in the spring-time?'

# A better view of seasons: Thankgiving, Spring Break, Summer Vacation, Christmas. I want to see data around seasonal
# usage.

# The most lucrative overall bookings for Mobile App is APAC and the highest Mobile Web is EMEA
# In general APAC loves Mobile, and they love the app. US/Europe, not so much


# Making a Pie Graphs showing the most profitable Super Region:


Super_Region_Pie = df.groupby(['Super Region'])['Net Gross Booking Value USD'].sum().sort_values(ascending=False)


# US acccounts for 33% of Net Gross Value
def Super_Region_Pie_Chart():
    mylabels = ["US", "APAC", "EMEA", "LATAM"]
    plt.pie(Super_Region_Pie, labels=mylabels, autopct='%1.0f%%')
    # plt.savefig('./Final_Project_Images/Super Region Net Gross Value Pie Chart.png')
    plt.show()


# Now a Bar Chart showing the most popular devices people use.
Platform_Pie = df.groupby(['Platform Type Name'])['Net Gross Booking Value USD'].sum().sort_values(ascending=False)


# We see Desktop accounts for 70% of hotel bookings. Mobile App and Mobile Web accounting for about the same.
def Platform_Pie_Chart():
    mylabels = ["Desktop", "Mobile Web", "Mobile App"]
    plt.pie(Platform_Pie, labels=mylabels, autopct='%1.0f%%')
    # x.savefig('./Final_Project_Images/Platform_Usage_Pie_Chart.jpg')
    plt.show()


# Now I want to make bar graphs showing the change from 2016 to 2017 so we can track growth.
# First 2016

df3 = df[df['Year'] == "2016"].groupby(['Super Region'])['Net Gross Booking Value USD'].sum().to_frame(name='2016')

df3['2017'] = df[df['Year'] == "2017"].groupby(['Super Region'])['Net Gross Booking Value USD'].sum()

# Now I am going to find out the change in growth from 2016 to 2017
df3['Percent_Change'] = (df3['2017'] / df3['2016'] - 1) * 100

df3['Super Region'] = df3.index


def Super_Region_Bar_2016():
    # Making my X and Y Axis for the bar chart
    x = df3['Super Region']
    y = df3['2016']
    plt.bar(x, y)
    plt.show()


# Now I am making the bar chart for 2017

def Super_Region_Bar_2017():
    # Here is my bar chart showing the revenue for each Super Region in 2016
    x = df3['Super Region']
    z = df3['2017']
    plt.bar(x, z)
    plt.show()





# Now I am making the bar chart showing the most growth in each region
def Percent_Change_Bar():
    x = df3['Super Region']
    j = df3['Percent_Change']
    # Here is my bar chart showing the revenue for each Super Region in 2016
    plt.bar(x, j)
    plt.show()


# Now I am going to make a new dataframe by Platform Type Name (Either Mobile App/Web or Desktop). Here is the 2016
# version
df4 = df[df['Year'] == "2016"].groupby(['Platform Type Name'])['Net Gross Booking Value USD'].sum().to_frame(
    name='2016')

# Now I'm going to make a dataframe by the 2017 version.
df4['2017'] = df[df['Year'] == "2017"].groupby(['Platform Type Name'])['Net Gross Booking Value USD'].sum()

# Calculating percent change from 2017 Platform to 2016 Platforms.
df4['Percent_Change'] = (df4['2017'] / df4['2016'] - 1) * 100

df4['Platform Type Name'] = df4.index

# Now I am going to chart out all the information from A,B,C and D.
A = df4['Platform Type Name']
B = df4['2016']
C = df4['2017']
D = df4['Percent_Change']


# Bar chart for 2016's Platform usage
def Platform_Type_2016():
    plt.bar(A, B)
    plt.show()




# Bar Chart for 2017's Platform Usage
def Platform_Type_2017():
    plt.bar(A, C)
    plt.show()


# Bar Chart for Percent Change of Platform Usage
def Platform_Type_Percent_Change():
    plt.bar(A, D)
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description='Gives the graphs from an Expedia Data File')

    parser.add_argument('command',
                        help='this will execute the command, you are going to want to use print')

    parser.add_argument('topic',
                        help='You can select which column you are interested in. Your choice is Region or'
                             'Platform')

    parser.add_argument('information', help='Select information you are looking for. Your options are BOOKINGS'
                                            'and GROWTH')

    args = parser.parse_args()

    if args.command == 'print':
        if args.topic == 'Region':
            if args.information == 'BOOKINGS':
                print('This is each Region by Net Booking Values')
                Super_Region_Pie_Chart()
            if args.information == 'GROWTH':
                print('Here is the performance from 2016, the performance of 2017 and the Growth from 2016 to 2017')
                Super_Region_Bar_2016()
                Super_Region_Bar_2017()
                Percent_Change_Bar()
        if args.topic == 'Platform':
            if args.information == 'BOOKINGS':
                print('This is each Platform by Net Booking Values')
                Platform_Pie_Chart()
            if args.information == 'GROWTH':
                print('Here is the performance from 2016, the performance of 2017 and the Growth from 2016 to 2017')
                Platform_Type_2016()
                Platform_Type_2017()
                Platform_Type_Percent_Change()


if __name__ == "__main__":
    main()
